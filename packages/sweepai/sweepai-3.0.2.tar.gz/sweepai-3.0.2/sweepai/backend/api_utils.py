import json
import os
import re
import traceback
from typing import Iterator, TypeVar

import git
import jsonpatch
import yaml
from diskcache import Cache
from fastapi import Header, HTTPException
from github import Github
from github.GithubException import GithubException
from loguru import logger

from sweepai.config.client import SweepConfig
from sweepai.config.server import (
    CACHE_DIRECTORY,
    CURL_CA_BUNDLE,
    GITHUB_API_BASE_URL,
    GITHUB_BASE_URL,
    WHITELISTED_USERS,
)
from sweepai.core.entities import FileChangeRequest, Snippet
from sweepai.core.github_utils import (
    ClonedRepo,
    CustomGithub,
    MockClonedRepo,
    get_github_client,
    get_installation_id,
)
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.modify.modify_utils import get_latest_contents
from sweepai.o11y.posthog_trace import posthog_trace
from sweepai.review.review_utils import split_diff_into_patches  # 0.4s import
from sweepai.search.agent.agent_utils import search_codebase
from sweepai.search.agent.search_prompts import pr_format
from sweepai.search.agent.summarize_directory import (
    recursively_summarize_directory,
    summarize_frameworks,
    summary_caches,
)
from sweepai.utils.diff import generate_diff, remove_whitespace_changes
from sweepai.utils.str_utils import pack_items_for_prompt, strip_triple_quotes
from sweepai.web.webhook_secret import hash_sha256

auth_cache = Cache(f"{CACHE_DIRECTORY}/auth_cache")
repo_cache = f"{CACHE_DIRECTORY}/repos"
message_cache = f"{CACHE_DIRECTORY}/messages"

T = TypeVar("T")

def get_cached_installation_id(org_name: str) -> str:
    return get_installation_id(org_name)


def get_github_client_from_org(org_name: str) -> tuple[str, CustomGithub]:
    return get_github_client(get_cached_installation_id(org_name))


def get_authenticated_github_client(repo_name: str, access_token: str):
    # Returns read access, write access, or none
    if access_token == "null":
        raise Exception("Access token is null")
    g = Github(access_token, base_url=GITHUB_API_BASE_URL)
    user = g.get_user()
    try:
        repo = g.get_repo(repo_name)
        return g
    except Exception:
        org_name, _ = repo_name.split("/")
        try:
            _token, g = get_github_client_from_org(org_name)
        except Exception:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch installation for {repo_name}. Make sure to install the app on this repository."
            )
        try:
            repo = g.get_repo(repo_name)
        except Exception as e:
            if "Not Found" in str(e):
                raise HTTPException(
                    status_code=404,
                    detail=f"Repository {repo_name} not found or not installed. Make sure to install the app on this repository."
                )
            raise HTTPException(
                status_code=400,
                detail=f"Error getting repo {repo_name}: {e}"
            )
        if repo.has_in_collaborators(user.login) or user.login in WHITELISTED_USERS:
            return g
        else:
            raise HTTPException(
                status_code=403,
                detail=f"User {user.login} does not have the necessary permissions for the repository {repo_name}."
            )


async def get_token_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token")
    return authorization.removeprefix("Bearer ")


def strip_branch_prefix(branch_name: str):
    return (
        branch_name.removeprefix("refs/heads/")
        .removeprefix("refs/tags/")
        .removeprefix("refs/remotes/")
        .removeprefix("origin/")
        .removeprefix("refs/")
    )


def check_valid_commit_sha(cloned_repo: ClonedRepo, commit_sha: str):
    try:
        cloned_repo.git_repo.git.cat_file(e=commit_sha)
        return True
    except git.GitCommandError:
        return False


def get_branch(cloned_repo: ClonedRepo, branch: str):
    try:
        return cloned_repo.github_repo.get_branch(branch)
    except GithubException as e:
        if e.status == 404:
            return None
        raise e


@posthog_trace
def check_repo_exists(
    username: str,
    repo_name: str,
    access_token: str,
    metadata: dict = {},
    do_clone: bool = False,
):
    # Can be refactored and re-used logic
    org_name, repo = repo_name.split("/")
    if os.path.exists(f"{repo_cache}/{repo}"):
        return {"success": True}
    try:
        if do_clone:
            print(f"Cloning {repo_name} to {repo_cache}/{repo}")
        else:
            print(f"Checking {repo_name}")
        os.environ["GIT_CURL_VERBOSE"] = "1"
        if do_clone or CURL_CA_BUNDLE:  # always clone with CURL_CA_BUNDLE, ls-remote does not work with it
            print("Cloning...")
            ClonedRepo.from_repo_full_name(repo_full_name=repo_name)
        if do_clone:
            print(f"Cloned {repo_name} to {repo_cache}/{repo}")
        else:
            print(f"Checked {repo_name}")
        return {"success": True}
    except git.GitCommandError as e:
        error_message = str(e)
        if "Repository not found" in error_message:
            return {"success": False, "error": "Repository not found"}
        elif "Invalid username or password" in error_message:
            return {"success": False, "error": "Invalid permissions"}
        else:
            return {"success": False, "error": f"Git error: {error_message}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def size_of_largest_change(patch: str):
    patches = split_diff_into_patches(patch, "")
    num_changes_per_patch = [patch.changes.count("\n+") + patch.changes.count("\n-") for patch in patches]
    return max(num_changes_per_patch) if num_changes_per_patch else 0


def get_pr_snippets(
    repo_name: str,
    annotations: dict,
    cloned_repo: ClonedRepo,
    context: ChatAgentContext = ChatAgentContext(use_case="ticket"),
):
    pr_snippets_with_change_size = []
    skipped_pr_snippets = []
    sweep_config = SweepConfig()
    pulls = annotations.get("pulls", [])
    pulls_messages: str = ""
    renamed_files: list[str] = []
    for pull in pulls:
        patch = pull["file_diffs"]
        diff_patch = ""
        # Filters copied from get_pr_changes
        for file_data in patch:
            file_path = file_data["filename"]
            if sweep_config.is_file_excluded(file_path):
                continue
            try:
                file_contents = cloned_repo.get_file_contents(file_path)
            except FileNotFoundError:
                logger.warning(f"Error getting file contents for {file_path}")
                continue
            is_file_suitable, reason = sweep_config.is_file_suitable(file_contents)
            if not is_file_suitable:
                continue
            diff = file_data.get("patch", "")
            if file_data["status"] == "renamed":
                new_file_name = file_data["filename"]
                old_file_name = file_data["previous_filename"]
                renamed_files.append(f"The file {old_file_name} was renamed to {new_file_name}.")
            elif file_data["status"] == "added":
                pr_snippets_with_change_size.append(
                    (
                        len(file_contents.split("\n")),
                        Snippet.from_file(file_path, file_contents, score=1),
                    )
                )
            elif file_data["status"] == "modified":
                patches = split_diff_into_patches(diff, file_path)
                num_changes_per_patch = [patch.changes.count("\n+") + patch.changes.count("\n-") for patch in patches]
                # Either the largest change is > 25 lines, or it changes more than 10% of the file
                if (
                    max(num_changes_per_patch, default=0) > 25
                    or file_data["changes"] / (file_contents.count("\n") + 1) > 0.1
                ):
                    # print(f"adding {file_path}")
                    # print(num_changes_per_patch)
                    # print(file_contents.count("\n"))
                    pr_snippets_with_change_size.append(
                        (
                            max(num_changes_per_patch, default=0),
                            Snippet.from_file(file_path, file_contents, score=1),
                        )
                    )
                else:
                    skipped_pr_snippets.append(Snippet.from_file(file_path, file_contents))
            if file_data["status"] in ("added", "modified", "removed"):
                diff_patch += f"File: {file_path}\n" + diff.strip("\n") + "\n\n"
        if diff_patch:
            pulls_messages += (
                pr_format.render(
                    title=pull["title"],
                    body=pull["body"],
                    patch=remove_whitespace_changes(diff_patch).strip("\n"),
                    url=f"https://{GITHUB_BASE_URL}/{repo_name}/pull/{pull['number']}",
                    use_case=context.use_case,
                )
                + "\n\n"
            )
            if renamed_files:
                renamed_files_string = "\n".join(renamed_files)
                pulls_messages += f"<renamed_files>{renamed_files_string}</renamed_files>\n\n"
    pr_snippets_with_change_size = sorted(pr_snippets_with_change_size, key=lambda x: x[0], reverse=True)
    pr_snippets = [snippet for _, snippet in pr_snippets_with_change_size]
    pr_snippets = pack_items_for_prompt(pr_snippets, lambda x: x.render(i=1), 100_000)
    return pr_snippets, skipped_pr_snippets, pulls_messages


# this is messy; its modular so we can move it elsewhere later
def get_repo_specific_description(cloned_repo: MockClonedRepo):
    try:
        sweep_yaml_contents = cloned_repo.get_file_contents("sweep.yaml")
        sweep_yaml = yaml.safe_load(sweep_yaml_contents)
        description = sweep_yaml.get("description", "")
        system_prompt_formatted_description = f"\nThis is a user provided description of the codebase. Keep this in mind if it is relevant to their query:\n<codebase_description>\n{description}\n</codebase_description>\n"
        return system_prompt_formatted_description
    except FileNotFoundError:
        logger.info(f"No .sweep.yaml file present in {cloned_repo.repo_full_name}.")
        return ""
    except Exception as e:
        logger.error(f"Error reading .sweep.yaml file: {e}")
        return ""


def stream_state_diff(
    stream: Iterator[T],
    initial_state: T = [],
) -> Iterator[T]:
    previous_state = initial_state
    try:
        for current_state in stream:
            patch = jsonpatch.JsonPatch.from_diff(previous_state, current_state)
            if patch:
                yield patch.to_string()
            previous_state = current_state
    except (Exception, KeyboardInterrupt) as e:
        yield json.dumps(
            [
                {
                    "status": "error",
                    "error": f"{str(e)}\n{str(traceback.format_exc())}",
                    "traceback": str(traceback.format_exc()),
                }
            ]
        )
        raise


def clean_code_suggestions(original_code: str, new_code: str, file_path: str, cloned_repo: ClonedRepo):
    try:
        file_contents = cloned_repo.get_file_contents(file_path)
    except FileNotFoundError:
        return original_code, new_code
    # this handles the case where the original code is a comment like "// the rest of the tests above"
    if (
        original_code.strip().count("\n") == 0
        and original_code not in file_contents
        and (original_code.strip().startswith("#") or original_code.strip().startswith("//"))
        and new_code.count("\n") > 0
    ):
        if original_code in new_code:
            return "", new_code.replace(original_code + "\n", "")
        return "", new_code
    return original_code, new_code


def extract_and_clean_code_suggestions(raw_suggestions: str, cloned_repo: ClonedRepo):
    pattern = r"<code_change>\s*<file_path>\n*(?P<filePath>[\s\S]+?)\n*</file_path>\s*(<justification>\n*(?P<justification>[\s\S]+?)\n*</justification>)?\s*(<original_code>\n*(?P<originalCode>[\s\S]*?)</original_code>\n*)?<new_code>\n*(?P<newCode>[\s\S]+?)\n*(</new_code>)?\s*</code_change>"
    # combine additions of the same file together
    code_suggestions_raw = [
        {
            "filePath": match_.groupdict().get("filePath", ""),
            "originalCode": strip_triple_quotes(match_.groupdict().get("originalCode") or ""),
            "newCode": strip_triple_quotes(match_.groupdict().get("newCode") or ""),
        }
        for match_ in re.finditer(pattern, raw_suggestions, re.DOTALL)
    ]
    new_code_suggestions_raw = []
    for code_suggestion in code_suggestions_raw:
        fcr = next(
            (
                fcr
                for fcr in new_code_suggestions_raw
                if fcr["filePath"] == code_suggestion["filePath"]
                and fcr["originalCode"] == code_suggestion["originalCode"] == ""
            ),
            None,
        )
        file_exists = False
        try:
            cloned_repo.get_file_contents(code_suggestion["filePath"])
            file_exists = True
        except FileNotFoundError:
            file_exists = False
        if fcr and not file_exists:
            fcr["newCode"] += "\n\n" + strip_triple_quotes(code_suggestion["newCode"])
        else:
            new_code_suggestions_raw.append(code_suggestion)
    code_suggestions_raw = new_code_suggestions_raw
    if code_suggestions_raw:
        code_suggestions = []
        for code_suggestion in code_suggestions_raw:
            original_code, new_code = clean_code_suggestions(
                strip_triple_quotes(code_suggestion["originalCode"]),
                strip_triple_quotes(code_suggestion["newCode"]),
                code_suggestion["filePath"],
                cloned_repo,
            )
            code_suggestions.append(
                {
                    "filePath": code_suggestion["filePath"],
                    "originalCode": original_code,
                    "newCode": new_code,
                    "state": "pending",
                    "error": None,
                    "id": "id_" + hash_sha256(code_suggestion["filePath"] + original_code + new_code),
                }
            )
        return code_suggestions
    return []


def validate_code_suggestions(
    code_suggestions: list,
    cloned_repo: ClonedRepo,
    modify_files_dict: FileModificationState,
    current_content: str,
):
    file_change_requests = []
    for code_suggestion in code_suggestions:
        try:
            file_contents = get_latest_contents(code_suggestion["filePath"], cloned_repo, modify_files_dict)
            if not file_contents:
                raise FileNotFoundError(f"File {code_suggestion['filePath']} not found.")
            change_type = "modify"
        except FileNotFoundError:
            change_type = "create"
        file_change_requests.append(
            FileChangeRequest(
                filename=code_suggestion["filePath"],
                instructions=f"<original_code>\n{code_suggestion['originalCode']}\n</original_code>\n<new_code>\n{code_suggestion['newCode']}\n</new_code>",
                change_type=change_type,
            )
        )
    return file_change_requests, current_content


def render_code_suggestions_for_logging(code_suggestions: list):
    """Render the diffs from old_code and new_code with file_path above"""
    rendered_suggestions = ""
    for suggestion in code_suggestions:
        suggestion_diff = generate_diff(
            suggestion["originalCode"], suggestion["newCode"]
        )
        suggestion_diff = suggestion_diff if suggestion_diff else "NO DIFF GENERATED"
        rendered_suggestion = f"File: {suggestion['filePath']}\n" + suggestion_diff
        rendered_suggestions += rendered_suggestion + "\n\n"
    return rendered_suggestions.strip()


def index_repo(repo_name: str, access_token: str):
    cloned_repo = ClonedRepo(repo_name, installation_id=-1, token=access_token)
    search_codebase("a", cloned_repo)
    recursively_summarize_directory([], cloned_repo)
    summarize_frameworks([], cloned_repo)


def get_directory_summaries(repo_name: str, directories: list[str]) -> dict[str, str]:
    key = ("summaries", repo_name)
    if key not in summary_caches:
        return {directory: "" for directory in directories}

    summaries, _ = summary_caches[key]
    return {directory: summaries.get(directory, "") for directory in directories}


if __name__ == "__main__":
    index_repo(os.environ.get("REPO"), os.environ.get("GITHUB_PAT"))
