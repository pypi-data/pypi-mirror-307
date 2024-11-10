from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property

import git
import requests
from github import (
    Github,
    GithubException,
    GithubIntegration,
    InputGitTreeElement,
    PullRequest,
)
from github.Auth import AppAuth, Token
from github.GithubException import BadCredentialsException, UnknownObjectException
from github.Repository import Repository

# get default_base_url from github
from github.Requester import Requester
from loguru import logger
from urllib3 import Retry

from sweepai.config.client import SweepConfig
from sweepai.config.server import (
    CACHE_DIRECTORY,
    CURL_CA_BUNDLE,
    GITHUB_API_BASE_URL,
    GITHUB_APP_ID,
    GITHUB_APP_PEM,
    GITHUB_BASE_URL,
)
from sweepai.core.entities import FileChangeRequest
from sweepai.o11y.log_utils import suppress_with_warning
from sweepai.utils.str_utils import get_hash

MAX_FILE_COUNT = 50

git_env = {"GIT_SSL_CAINFO": CURL_CA_BUNDLE} if CURL_CA_BUNDLE else {}

all_repos: list[ClonedRepo] = []  # list of all ClonedRepo objects

auth = AppAuth(app_id=GITHUB_APP_ID, private_key=GITHUB_APP_PEM) if GITHUB_APP_ID and GITHUB_APP_PEM else None
github_integration = GithubIntegration(auth=auth, base_url=GITHUB_API_BASE_URL) if auth else None


def make_valid_string(string: str):
    pattern = r"[^\w./-]+"
    return re.sub(pattern, "_", string)


def get_jwt(signing_key: str = "", app_id: str = ""):
    from jwt import encode

    if not signing_key:
        signing_key = GITHUB_APP_PEM
    if not app_id:
        app_id = GITHUB_APP_ID
    # max is 10 minutes, use 5 minutes to be very safe. 9min 50sec failed before
    payload = {"iat": int(time.time()), "exp": int(time.time()) + 300, "iss": app_id}
    return encode(payload, signing_key, algorithm="RS256")


def get_token(installation_id: int, signing_key: str = "", app_id: str = ""):
    if int(installation_id) < 0:
        logger.warning(f"installation_id is {installation_id}, using GITHUB_PAT instead.")
        return os.environ["GITHUB_PAT"]
    for timeout in [5.5, 5.5, 10.5]:
        try:
            jwt = get_jwt(signing_key=signing_key, app_id=app_id)
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + jwt,
                "X-GitHub-Api-Version": "2022-11-28",
            }
            response = requests.post(
                f"{GITHUB_API_BASE_URL}/app/installations/{int(installation_id)}/access_tokens",
                headers=headers,
            )
            obj = response.json()
            if "token" not in obj:
                logger.error(obj)
                raise Exception("Could not get token")
            return obj["token"]
        except SystemExit:
            raise SystemExit
        except Exception:
            time.sleep(timeout)
    signing_key = GITHUB_APP_PEM
    app_id = GITHUB_APP_ID
    exception_message = "Could not get token."
    if not signing_key:
        exception_message += " Missing GITHUB_APP_PEM in the .env file."
    if not app_id:
        exception_message += " Missing GITHUB_APP_ID in the .env file."
    if signing_key and app_id:
        exception_message += "Please double check that Sweep has the correct permissions to access your repository."

    raise Exception(exception_message)


def get_app(signing_key: str = "", app_id: str = ""):
    jwt = get_jwt(signing_key=signing_key, app_id=app_id)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + jwt,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(f"{GITHUB_API_BASE_URL}/app", headers=headers)
    return response.json()


def get_github(repo_full_name: str):
    org_name, repo_name = repo_full_name.split("/")
    return CustomGithub(installation_id=get_installation_id(username=org_name), base_url=GITHUB_API_BASE_URL)


def get_github_repo_object(repo_full_name: str):
    g = get_github(repo_full_name)
    return g.get_repo(repo_full_name)


class CustomRequester(Requester):
    def __init__(
        self,
        token,
        timeout: int = 15,
        user_agent: str = "PyGithub/Python",
        per_page: int = 30,
        verify: bool = True,
        retry=None,
        pool_size=None,
        installation_id: int = None,
    ) -> "CustomRequester":
        self.token = token
        self.installation_id = installation_id
        base_url = GITHUB_API_BASE_URL
        auth = Token(token)
        retry = Retry(
            total=3,
        )  # 3 retries
        self.timeout = timeout
        self.user_agent = user_agent
        self.per_page = per_page
        self.verify = verify
        self.retry = retry
        self.pool_size = pool_size
        super().__init__(
            auth=auth,
            base_url=base_url,
            timeout=timeout,
            user_agent=user_agent,
            per_page=per_page,
            verify=verify,
            retry=retry,
            pool_size=pool_size,
        )

    def _refresh_token(self):
        """Get a new token and reinitialize the requester with it"""
        try:
            self.token = github_integration.get_access_token(self.installation_id).token
        except Exception:
            logger.warning("[YELLOW] Could not get access token from GitHub API using PyGithub, using legacy method")
            self.token = get_token(self.installation_id, signing_key=GITHUB_APP_PEM, app_id=GITHUB_APP_ID)
        
        # Reinitialize with new token
        auth = Token(self.token)
        super().__init__(
            auth=auth,
            base_url=GITHUB_API_BASE_URL,
            timeout=self.timeout,
            user_agent=self.user_agent,
            per_page=self.per_page,
            verify=self.verify,
            retry=self.retry,
            pool_size=self.pool_size,
        )

    def requestJsonAndCheck(self, *args, **kwargs):
        try:
            return super().requestJsonAndCheck(*args, **kwargs)
        except (BadCredentialsException, UnknownObjectException) as e:
            if isinstance(e, BadCredentialsException) or (
                isinstance(e, UnknownObjectException) and e.status in (401, 403)
            ):
                self._refresh_token()
                return super().requestJsonAndCheck(*args, **kwargs)
            raise e


class CustomGithub(Github):
    def __init__(
        self,
        installation_id: int,
        base_url: str = GITHUB_API_BASE_URL,
        *args,
        **kwargs,
    ) -> "CustomGithub":
        self.installation_id = installation_id
        self.token = self._get_token()
        
        # Create our custom requester first
        requester = CustomRequester(
            self.token, 
            installation_id=self.installation_id,
        )
        
        # Initialize with the requester directly
        self._Github__requester = requester

    @classmethod
    def from_repo_full_name(cls, repo_full_name: str, **kwargs):
        org_name, repo_name = repo_full_name.split("/")
        try:
            installation_id = github_integration.get_repo_installation(org_name, repo_name).id
        except Exception:
            logger.warning("[YELLOW] Could not get access token from GitHub API using PyGithub, using legacy method")
            installation_id = get_installation_id(org_name)
        return cls(installation_id, **kwargs)

    def _get_token(self) -> str:
        try:
            return github_integration.get_access_token(self.installation_id).token
        except Exception:
            logger.warning("[YELLOW] Could not get access token from GitHub API using PyGithub, using legacy method")
            return get_token(self.installation_id, signing_key=GITHUB_APP_PEM, app_id=GITHUB_APP_ID)

def get_github_client(
    installation_id: int, 
) -> tuple[str, CustomGithub]:
    github_instance = CustomGithub(
        installation_id,
    )
    return github_instance.token, github_instance


# fetch installation object
def get_installation(username: str, signing_key: str = "", app_id: str = ""):
    jwt = get_jwt(signing_key=signing_key, app_id=app_id)
    try:
        # Try user
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/users/{username}/installation",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + jwt,
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        obj = response.json()
        return obj
    except Exception:
        # Try org
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/orgs/{username}/installation",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + jwt,
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            obj = response.json()
            return obj["id"]
        except Exception as e:
            logger.error(e)
            logger.error(response.text)
        raise Exception("Could not get installation, probably not installed")


def get_installation_id(username: str) -> int:
    jwt = get_jwt(signing_key=GITHUB_APP_PEM, app_id=GITHUB_APP_ID)
    try:
        # Try user
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/users/{username}/installation",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + jwt,
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        obj = response.json()
        return obj["id"]
    except Exception as e:
        logger.info(e)
        # Try org
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/orgs/{username}/installation",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + jwt,
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            obj = response.json()
            return obj["id"]
        except Exception as e:
            logger.error(e)
            logger.error(response.text)
        raise Exception("Could not get installation, probably not installed")


# for check if a file exists within a github repo (calls the actual github api)
def file_exists_in_repo(repo: Repository, filepath: str):
    try:
        # Attempt to get the contents of the file
        repo.get_contents(filepath)
        return True  # If no exception, the file exists
    except GithubException:
        return False  # File does not exist


def validate_and_sanitize_multi_file_changes(
    repo: Repository, file_changes: dict[str, str], fcrs: list[FileChangeRequest]
):
    sanitized_file_changes = {}
    all_file_names = list(file_changes.keys())
    all_fcr_file_names = set(os.path.normpath(fcr.filename) for fcr in fcrs)
    file_removed = False
    # validate each file change
    for file_name in all_file_names:
        # file_name must either appear in the repo or in a fcr
        if os.path.normpath(file_name) in all_fcr_file_names or file_exists_in_repo(repo, os.path.normpath(file_name)):
            sanitized_file_changes[file_name] = copy.deepcopy(file_changes[file_name])
        else:
            file_removed = True
    return sanitized_file_changes, file_removed


# commits multiple files in a single commit, returns the commit object
def commit_multi_file_changes(
    cloned_repo: "ClonedRepo",
    file_changes: dict[str, str],
    commit_message: str,
    branch: str,
    renames_dict: dict[str, str] = {},
):
    assert file_changes or renames_dict
    repo: Repository = cloned_repo.github_repo
    if renames_dict:
        blobs_to_commit = []
        # make a separate commit with just the renames
        for old_name, new_name in renames_dict.items():
            file_contents = cloned_repo.get_file_contents(new_name)
            blob = repo.create_git_blob(file_contents, "utf-8")
            blobs_to_commit.append(
                InputGitTreeElement(
                    path=os.path.normpath(old_name).lstrip("/"),
                    mode="100644",
                    type="blob",
                    sha=None,
                )
            )
            blobs_to_commit.append(
                InputGitTreeElement(
                    path=os.path.normpath(new_name).lstrip("/"),
                    mode="100644",
                    type="blob",
                    sha=blob.sha,
                )
            )
        head_sha = repo.get_branch(branch).commit.sha
        base_tree = repo.get_git_tree(sha=head_sha)
        # create new git tree
        new_tree = repo.create_git_tree(blobs_to_commit, base_tree=base_tree)
        # commit the changes
        parent = repo.get_git_commit(sha=head_sha)
        commit_message = "Renamed to " + ", ".join(renames_dict.values())
        commit_message = commit_message[:69] + "..." if len(commit_message) > 70 else commit_message
        commit = repo.create_git_commit(
            commit_message,
            new_tree,
            [parent],
        )
        # update ref of branch
        ref = f"heads/{branch}"
        repo.get_git_ref(ref).edit(sha=commit.sha)
        if not file_changes:
            return commit
    blobs_to_commit = []
    # convert to blob
    for path, content in file_changes.items():
        blob = repo.create_git_blob(content, "utf-8")
        blobs_to_commit.append(
            InputGitTreeElement(
                path=os.path.normpath(path).lstrip("/"),
                mode="100644",
                type="blob",
                sha=blob.sha,
            )
        )
    head_sha = repo.get_branch(branch).commit.sha
    base_tree = repo.get_git_tree(sha=head_sha)
    # create new git tree
    new_tree = repo.create_git_tree(blobs_to_commit, base_tree=base_tree)
    # commit the changes
    parent = repo.get_git_commit(sha=head_sha)
    commit = repo.create_git_commit(
        commit_message,
        new_tree,
        [parent],
    )
    # update ref of branch
    ref = f"heads/{branch}"
    repo.get_git_ref(ref).edit(sha=commit.sha)
    return commit


def clean_branch_name(branch: str) -> str:
    branch = re.sub(r"[^a-zA-Z0-9_\-/]", "-", branch)
    branch = re.sub(r"-+", "-", branch)
    branch = branch.strip("-")

    return branch


def generate_new_branch_name(repo: Repository, branch: str, base_branch: str, MAX_RETRIES: int = 10):
    """
    Try placing hashes after to get a unique branch name.
    """
    base_branch_obj = repo.get_branch(base_branch)
    for _ in range(MAX_RETRIES):
        with suppress_with_warning(GithubException):
            _hash = get_hash()[:5]
            new_branch_name = f"{branch}_{_hash}"
            logger.warning(f"Retrying {new_branch_name}...")
            repo.create_git_ref(f"refs/heads/{new_branch_name}", base_branch_obj.commit.sha)
            return repo.get_branch(new_branch_name)
    raise Exception(f"Could not create branch {branch} on {repo.full_name} after {MAX_RETRIES} retries")


def create_and_get_branch(repo: Repository, branch: str, base_branch: str = ""):
    # Creates a new branch, changes name if it already exists
    branch = clean_branch_name(branch)
    base_branch = base_branch or repo.default_branch
    try:
        repo.get_branch(branch)
    except GithubException:
        # Branch doesn't exist, expected
        base_branch_obj = repo.get_branch(base_branch)
        repo.create_git_ref(f"refs/heads/{branch}", base_branch_obj.commit.sha)
        return repo.get_branch(branch)
    else:
        # Branch exists, create a new name
        return generate_new_branch_name(repo, branch, base_branch)


REPO_CACHE_BASE_DIR = os.path.join(CACHE_DIRECTORY, "repos")


@contextmanager
def temporary_cloned_repo_copy(original_repo: ClonedRepo):
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.debug(f"Copying {original_repo.repo_dir} to {temp_dir}")
        try:
            copy_with_shutil_backoff(original_repo.repo_dir, temp_dir)
            base_name = os.path.basename(original_repo.repo_dir)
            new_repo_dir = os.path.join(temp_dir, base_name)
            temp_repo = MockClonedRepo(
                _repo_dir=new_repo_dir,
                repo_full_name=original_repo.repo_full_name,
                installation_id=original_repo.installation_id,
                branch=original_repo.branch,
                token=original_repo.token,
            )
            temp_repo.git_repo.git.remote("set-url", "origin", original_repo.clone_url, env=git_env)
            yield temp_repo
        except subprocess.CalledProcessError as e:
            logger.info(f"Error copying repo: {e.stderr}")
            raise
        except Exception as e:
            logger.info(f"Unexpected error: {str(e)}")
            raise


def get_github_repo(repo_full_name: str):
    username = repo_full_name.split("/")[0]
    return CustomGithub(installation_id=get_installation_id(username=username), base_url=GITHUB_API_BASE_URL).get_repo(repo_full_name)


def has_repo_been_cloned_before(repo_full_name: str, branch: str | None = None):
    github_repo = get_github_repo(repo_full_name=repo_full_name)
    branch = branch or SweepConfig.get_branch(github_repo)
    return os.path.exists(os.path.join(REPO_CACHE_BASE_DIR, repo_full_name, "base", parse_collection_name(branch)))


def copy_with_shutil_backoff(cached_dir: str, repo_dir: str):
    """Raises the error from subprocess.run if it fails"""
    try:
        subprocess.run(
            # -R is recursive, -v is verbose, -P is preserve symlinks (no dereferencing)
            ["cp", "-Rv", "-P", cached_dir, repo_dir],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as e1:
        # backoff to shutil if cp fails
        try:
            subprocess.run(["rm", "-rf", repo_dir], check=True)
            logger.warning(f"[YELLOW] Error copying repo: {e1}, falling back to shutil")
            shutil.copytree(src=cached_dir, dst=repo_dir, symlinks=True)
        except Exception as e2:
            logger.error(f"Error copying repo: {e1}, {e2}")
            raise e1


@dataclass
class ClonedRepo:
    repo_full_name: str
    branch: str | None = None
    installation_id: str | None = None
    token: str | None = None
    github_repo: Repository | None = None
    git_repo: git.Repo | None = None

    class Config:
        arbitrary_types_allowed = True

    @cached_property
    def cached_dir(self):
        return os.path.join(
            REPO_CACHE_BASE_DIR,
            self.repo_full_name,
            "base",
            self.default_branch,
        )

    @cached_property
    def repo_dir(self):  # pylint: disable=method-hidden
        commit_sha = (
            self.github_repo.get_branch(self.branch).commit.sha
            or self.github_repo.get_commit(self.branch).sha
            or "latest"
        )
        return os.path.join(
            REPO_CACHE_BASE_DIR,
            self.repo_full_name,
            commit_sha,
        )

    @property
    def repo_name(self):
        # just get the repo name from the repo_full_name without org_name
        return self.repo_full_name.split("/")[1]

    @property
    def clone_url(self):
        return f"https://x-access-token:{self.token}@{GITHUB_BASE_URL}/{self.repo_full_name}.git"

    @cached_property
    def current_commit_sha(self):
        return self.git_repo.git.rev_parse("HEAD")

    @cached_property
    def cache_key(self):
        return f"{self.repo_full_name}:{self.current_commit_sha}"

    @property
    def default_branch(self):
        return self.github_repo.default_branch

    def clone(self):
        if is_valid_git_repo(self.cached_dir):
            git_repo = git.Repo(self.cached_dir)
        else:
            subprocess.run(["rm", "-rf", self.cached_dir])
            git_repo = git.Repo.clone_from(
                self.clone_url,
                self.cached_dir,
                env=git_env,
                multi_options=["--recurse-submodules"],
            )

        # Check whether cached_dir needs to be updated
        latest_commit = self.github_repo.get_commit(self.default_branch).sha
        cached_dir_commit = git_repo.git.rev_parse("HEAD")
        should_pull_latest_cached_dir = not (latest_commit == cached_dir_commit)
        if should_pull_latest_cached_dir:
            logger.info("Cached directory is outdated, pulling cached_dir...")
            try:
                git_repo.git.remote("set-url", "origin", self.clone_url, env=git_env)
                git_repo.git.clean("-fd")
                git_repo.git.checkout(self.default_branch, env=git_env)
                git_repo.git.reset("--hard", f"origin/{self.default_branch}", env=git_env)
                git_repo.git.pull(env=git_env)
            except Exception as e:
                logger.error(f"Error pulling cached_dir: {e}")
                raise Exception("Error pulling cached_dir")

        if is_valid_git_repo(self.repo_dir):
            git_repo = git.Repo(self.repo_dir)
        else:
            logger.warning(f"Invalid git repository: {self.repo_dir}")
            self.delete_and_copy_latest_cached_dir_to_repo_dir()
            git_repo = git.Repo(self.repo_dir)
        
        try:
            git_repo.git.remote("set-url", "origin", self.clone_url, env=git_env)
        except Exception as e:
            logger.error(f"Error setting remote URL: {e}")
        return git_repo

    def __post_init__(self):
        subprocess.run(["git", "config", "--global", "http.postBuffer", "524288000"])
        if self.installation_id:
            self.token = self.token or get_token(self.installation_id)
        # Try to get the github repo from cache
        self.github_repo = self.github_repo or get_github_repo(repo_full_name=self.repo_full_name)
        self.branch = self.branch or SweepConfig.get_branch(self.github_repo)
        self.git_repo: git.Repo = self.clone()
        all_repos.append(self)
        if self.branch != self.default_branch:
            self.safely_checkout_to_non_default_branch(self.github_repo.get_branch(self.branch).commit.sha)

    def delete_and_copy_latest_cached_dir_to_repo_dir(self):
        if os.path.exists(self.repo_dir):
            logger.info(f"Repo directory {self.repo_dir} exists but is empty, deleting...")
            subprocess.run(["rm", "-rf", self.repo_dir])
        logger.info("Copying repo...")
        logger.debug(f"Copying {self.cached_dir} to {self.repo_dir}")
        os.makedirs(os.path.dirname(self.repo_dir), exist_ok=True)
        try:
            copy_with_shutil_backoff(self.cached_dir, self.repo_dir)
        except Exception as e:
            # we need this check since sometimes gitignored files still "exist" via symlinks
            if "No such file or directory" in str(e):
                pass
            else:
                logger.info(f"Error copying repo {str(e)}")
                raise e
        assert os.path.exists(self.repo_dir) and len(os.listdir(self.repo_dir)) > 0
        logger.info("Done copying")

    def handle_checkout_failures(self):
        untracked_files = self.git_repo.untracked_files
        if untracked_files:
            logger.info(f"Untracked files found: {', '.join(untracked_files)}")
            for file in untracked_files:
                file_path = os.path.join(self.git_repo.working_dir, file)
                if os.path.isfile(file_path):
                    logger.info(f"Removing untracked file: {file}")
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    logger.info(f"Removing untracked directory: {file}")
                    os.removedirs(file_path)
        else:
            logger.info("No untracked files found")

        # if the index.lock file exists, delete it
        index_lock_file = os.path.join(self.git_repo.working_dir, "index.lock")
        if os.path.exists(index_lock_file):
            logger.info(f"Removing index lock file: {index_lock_file}")
            os.remove(index_lock_file)

        logger.info("Cleaning untracked files")
        self.git_repo.git.clean("-fd")

    @classmethod
    def from_repo_full_name(cls, repo_full_name: str, branch: str | None = None):
        g = CustomGithub.from_repo_full_name(repo_full_name)
        repo = g.get_repo(repo_full_name)
        branch = branch or repo.default_branch
        return cls(
            repo_full_name,
            branch=branch,
            installation_id=g.installation_id,
            token=g.token,
            github_repo=repo,
        )

    def safely_checkout_to_non_default_branch(self, branch_commit_sha: str):
        branch_commit_repo_dir = os.path.join(REPO_CACHE_BASE_DIR, self.repo_full_name, branch_commit_sha)
        self.repo_dir = branch_commit_repo_dir
        # Ensure the git repo is valid, copy it over if not
        if not is_valid_git_repo(self.repo_dir):
            try:
                # copy the cached_dir to the repo_dir
                self.delete_and_copy_latest_cached_dir_to_repo_dir()
            except subprocess.CalledProcessError as e:
                error_message = f"Command '{e.cmd}' failed with exit status {e.returncode}.\n"
                error_message += f"STDOUT: {e.stdout}\n"
                error_message += f"STDERR: {e.stderr}"
                logger.error(f"Error copying repo: {error_message}")
                raise e
        # This should always be a valid git_repo now
        self.git_repo = git.Repo(self.repo_dir)
        # Checkout to the branch_commit_sha and setup the origin
        try:
            self.git_repo.git.remote("set-url", "origin", self.clone_url, env=git_env)
            self.git_repo.git.fetch("origin", branch_commit_sha, env=git_env)
            self.git_repo.git.checkout(branch_commit_sha, env=git_env)
        except Exception as e:
            logger.error(f"Error checking out branch {branch_commit_sha}: {e}")
            raise
        return

    def delete_repo_on_disk(self):
        # you can't use any packages here since this is called during __del__, so os becomes a NoneType and os.path is a NPE
        try:
            if os.path.exists(self.repo_dir) and not isinstance(self.repo_dir, tempfile.TemporaryDirectory):
                logger.info(f"Deleting repo {self.repo_dir}")
                subprocess.Popen(
                    ["rm", "-rf", self.repo_dir],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    preexec_fn=os.setsid,
                )
                return True
            else:
                logger.info(f"Repo {self.repo_dir} does not exist or is a TemporaryDirectory.")
                return False
        except Exception as e:
            # I use print because on shutdown loguru might have been set to none already
            print(f"Failed to delete {self.repo_dir}: {str(e)}")
            return False

    @contextmanager
    def cleanup_context(self):
        try:
            yield self
        finally:
            self.delete_repo_on_disk()

    def get_file_list(self):
        root_directory = self.repo_dir
        files: list[str] = []
        sweep_config: SweepConfig = SweepConfig()

        def dfs_helper(directory):
            nonlocal files
            for item in os.listdir(directory):
                if item == ".git":
                    continue
                if item in sweep_config.exclude_dirs:  # this saves a lot of time
                    continue
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    # make sure the item_path is not in one of the banned directories
                    if not sweep_config.is_file_excluded(item_path):
                        files.append(item_path)  # Add the file to the list
                elif os.path.isdir(item_path):
                    dfs_helper(item_path)  # Recursive call to explore subdirectory

        dfs_helper(root_directory)
        files = [file[len(root_directory) + 1 :] for file in files]
        return files

    def get_directory_list(self):
        root_directory = self.repo_dir
        files = []
        sweep_config: SweepConfig = SweepConfig()

        def dfs_helper(directory):
            nonlocal files
            for item in os.listdir(directory):
                if item == ".git":
                    continue
                if item in sweep_config.exclude_dirs:  # this saves a lot of time
                    continue
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    files.append(item_path)  # Add the file to the list
                    dfs_helper(item_path)  # Recursive call to explore subdirectory

        dfs_helper(root_directory)
        files = [file[len(root_directory) + 1 :] for file in files]
        return files

    def get_immediate_subdirs(self):
        # fast way to get all immediate subdirs without a dfs
        return [name for name in os.listdir(self.repo_dir) if os.path.isdir(os.path.join(self.repo_dir, name))]

    def get_file_contents(self, file_path, ref=None):
        local_path = os.path.join(self.repo_dir, file_path.lstrip("/"))
        if os.path.exists(local_path) and os.path.isfile(local_path):
            with open(local_path, "r", encoding="utf-8", errors="replace") as f:
                contents = f.read()
            return contents
        else:
            raise FileNotFoundError(f"{local_path} does not exist.")

    def get_num_files_from_repo(self):
        # subprocess.run(["git", "config", "--global", "http.postBuffer", "524288000"])
        self.git_repo.git.checkout(self.default_branch)
        file_list = self.get_file_list()
        return len(file_list)

    def get_commit_history(self, username: str = "", limit: int = 200, time_limited: bool = True):
        commit_history = []
        try:
            if username != "":
                commit_list = list(self.git_repo.iter_commits(author=username))
            else:
                commit_list = list(self.git_repo.iter_commits())
            line_count = 0
            cut_off_date = datetime.now() - timedelta(days=7)
            for commit in commit_list:
                # must be within a week
                if time_limited and commit.authored_datetime.replace(tzinfo=None) <= cut_off_date.replace(tzinfo=None):
                    logger.info("Exceeded cut off date, stopping...")
                    break
                repo = get_github_client(self.installation_id)[1].get_repo(self.repo_full_name)
                branch = SweepConfig.get_branch(repo)
                if branch not in self.git_repo.git.branch():
                    branch = f"origin/{branch}"
                diff = self.git_repo.git.diff(commit, branch, unified=1)
                lines = diff.count("\n")
                # total diff lines must not exceed 200
                if lines + line_count > limit:
                    logger.info(f"Exceeded {limit} lines of diff, stopping...")
                    break
                commit_history.append(
                    f"<commit>\nAuthor: {commit.author.name}\nMessage: {commit.message}\n{diff}\n</commit>"
                )
                line_count += lines
        except Exception:
            logger.error(f"An error occurred: {traceback.print_exc()}")
        return commit_history

    def get_similar_directories(self, file_path: str, limit: int = 5):
        from rapidfuzz.fuzz import QRatio

        # Fuzzy search over file names
        # file_name = os.path.basename(file_path)
        all_file_paths = self.get_directory_list()

        # get top limit similar directories
        sorted_file_paths = sorted(
            all_file_paths,
            key=lambda file_name_: QRatio(file_name_, file_path),
            reverse=True,
        )

        filtered_file_paths = list(filter(lambda file_name_: QRatio(file_name_, file_path) > 50, sorted_file_paths))

        return filtered_file_paths[:limit]

    def get_similar_file_paths(self, file_path: str, limit: int = 10):
        from rapidfuzz.fuzz import ratio

        # Fuzzy search over file names
        file_name = os.path.basename(file_path)
        all_file_paths = self.get_file_list()
        # filter for matching extensions if both have extensions
        if "." in file_name:
            all_file_paths = [
                file for file in all_file_paths if "." in file and file.split(".")[-1] == file_name.split(".")[-1]
            ]
        files_with_matching_name = []
        files_without_matching_name = []
        for file_path in all_file_paths:
            if file_name in file_path:
                files_with_matching_name.append(file_path)
            else:
                files_without_matching_name.append(file_path)
        file_path_to_ratio = {file: ratio(file_name, file) for file in all_file_paths}
        files_with_matching_name = sorted(
            files_with_matching_name,
            key=lambda file_path: file_path_to_ratio[file_path],
            reverse=True,
        )
        files_without_matching_name = sorted(
            files_without_matching_name,
            key=lambda file_path: file_path_to_ratio[file_path],
            reverse=True,
        )
        # this allows 'config.py' to return 'sweepai/config/server.py', 'sweepai/config/client.py', 'sweepai/config/__init__.py' and no more
        filtered_files_without_matching_name = list(
            filter(
                lambda file_path: file_path_to_ratio[file_path] > 50,
                files_without_matching_name,
            )
        )
        all_files = files_with_matching_name + filtered_files_without_matching_name
        return all_files[:limit]


# updates a file with new_contents, returns True if successful
def update_file(root_dir: str, file_path: str, new_contents: str):
    local_path = os.path.join(root_dir, file_path)
    try:
        with open(local_path, "w") as f:
            f.write(new_contents)
        return True
    except Exception as e:
        logger.error(f"Failed to update file: {e}")
        return False

def is_valid_git_repo(repo_path: str) -> bool:
    """
    Checks if a directory is a valid git repository by verifying:
    1. .git directory exists and has required files
    2. git commands can be executed
    3. repository has a valid HEAD reference
    4. repository has valid objects and refs
    """
    try:
        # Check if directory exists
        if not os.path.exists(repo_path):
            return False
            
        # Check for .git directory and critical files
        git_dir = os.path.join(repo_path, ".git")
        required_git_files = [
            os.path.join(git_dir, "HEAD"),  # HEAD reference file
            os.path.join(git_dir, "config"),  # Git config
            os.path.join(git_dir, "refs"),  # refs directory
            os.path.join(git_dir, "objects"),  # objects directory
        ]
        
        if not all(os.path.exists(f) for f in required_git_files):
            return False
            
        # Try to initialize repo object
        repo = git.Repo(repo_path)
        
        # Check if HEAD is valid
        if repo.head.is_valid():
            try:
                # Try to get current branch name
                _ = repo.active_branch.name
            except TypeError:
                # HEAD exists but might be detached
                pass
        
        return True
        
    except (git.InvalidGitRepositoryError, git.NoSuchPathError) as e:
        logger.warning(f"Invalid git repository: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while validating git repo: {str(e)}")
        return False


@dataclass
class MockClonedRepo(ClonedRepo):
    _repo_dir: str = ""
    git_repo: git.Repo | None = None

    def __init__(
        self,
        _repo_dir: str,
        repo_full_name: str,
        installation_id: str = "",
        branch: str | None = None,
        token: str | None = None,
        repo: Repository | None = None,
    ):
        self._repo_dir = _repo_dir
        self.repo_full_name = repo_full_name
        self.installation_id = installation_id
        self.branch = branch
        self.token = token
        if repo:
            self.github_repo = repo
        else:
            try:
                org_name, repo_name = self.repo_full_name.split("/")
                installation = github_integration.get_repo_installation(org_name, repo_name)
                self.github_repo = installation.get_github_for_installation().get_repo(self.repo_full_name)
            except Exception as e:
                logger.warning(f"[YELLOW] Failed to get github repo for {self.repo_full_name}: {str(e)}")
                self.github_repo = None
        self.git_repo = git.Repo(self.repo_dir)

    @classmethod
    def from_dir(cls, repo_dir: str, **kwargs):
        return cls(_repo_dir=repo_dir, **kwargs)

    @property
    def cached_dir(self):
        return self._repo_dir

    @property
    def repo_dir(self):
        return self._repo_dir

    def clone(self):
        return git.Repo(self.repo_dir)

    def __post_init__(self):
        return self

    def __del__(self):
        return True


def parse_collection_name(name: str) -> str:
    # Replace any non-alphanumeric characters with hyphens
    name = re.sub(r"[^\w-]", "--", name)
    # Ensure the name is between 3 and 63 characters and starts/ends with alphanumeric
    name = re.sub(r"^(-*\w{0,61}\w)-*$", r"\1", name[:63].ljust(3, "x"))
    return name


# set whether or not a pr is a draft, there is no way to do this using pygithub
def convert_pr_draft_field(pr: PullRequest, is_draft: bool = False, installation_id: int = 0) -> bool:
    token = get_token(installation_id)
    pr_id = pr.raw_data["node_id"]
    # GraphQL mutation for marking a PR as ready for review
    mutation = """
    mutation MarkPRReady {
    markPullRequestReadyForReview(input: {pullRequestId: {pull_request_id}}) {
    pullRequest {
    id
    }
    }
    }
    """.replace(
        "{pull_request_id}", '"' + pr_id + '"'
    )

    # GraphQL API URL
    url = f"{GITHUB_API_BASE_URL}/graphql"

    # Headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Prepare the JSON payload
    json_data = {
        "query": mutation,
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(json_data))
    if response.status_code != 200:
        logger.error(f"Failed to convert PR to {'draft' if is_draft else 'open'}")
        return False
    return True


### REVIEW RELATED


# get the review threads obejct for a pr, required to tell if a comment is resolved or not
def get_review_threads(repo_full_name: str, pr_number: int, installation_id: int):
    token = get_token(installation_id)
    query = """
query GetReviewThreads($owner: String!, $name: String!, $prNumber: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $prNumber) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 100) {
            nodes {
              id
              body
              author {
                login
              }
              createdAt
            }
          }
        }
      }
    }
  }
}
    """

    # GraphQL API URL
    url = f"{GITHUB_API_BASE_URL}/graphql"

    # Headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    owner, name = repo_full_name.split("/")
    # Prepare the JSON payload
    variables = {"owner": owner, "name": name, "prNumber": pr_number}
    json_data = {"query": query, "variables": variables}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(json_data))
    if response.status_code != 200:
        return {}
    review_threads_json = response.json()["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
    return review_threads_json


# refresh user token, github client and repo object
def refresh_token(repo_full_name: str, installation_id: int):
    user_token, g = get_github_client(installation_id)
    repo = g.get_repo(repo_full_name)
    return user_token, g, repo


if __name__ == "__main__":
    try:
        organization_name = "sweepai"
        sweep_config = SweepConfig()
        installation_id = get_installation_id(organization_name)
        user_token, g = get_github_client(installation_id)
        cloned_repo = ClonedRepo("sweepai/sweep", installation_id, "main")
        commit_history = cloned_repo.get_commit_history()
        similar_file_paths = cloned_repo.get_similar_file_paths("config.py")
        # ensure no similar file_paths are sweep excluded
        assert not any([file for file in similar_file_paths if sweep_config.is_file_excluded(file)])
        print(f"similar_file_paths: {similar_file_paths}")
        str1 = "a\nline1\nline2\nline3\nline4\nline5\nline6\ntest\n"
        str2 = "a\nline1\nlineTwo\nline3\nline4\nline5\nlineSix\ntset\n"
        mocked_repo = MockClonedRepo.from_dir(
            cloned_repo.repo_dir,
            repo_full_name="sweepai/sweep",
        )
        print(f"mocked repo: {mocked_repo}")
    except Exception as e:
        logger.error(f"github_utils.py failed to run successfully with error: {e}")
