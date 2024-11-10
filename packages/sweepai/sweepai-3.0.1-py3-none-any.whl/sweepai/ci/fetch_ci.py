import io
import re
import ssl
import zipfile
from contextlib import suppress
from functools import lru_cache
from time import sleep
from urllib.parse import urlparse, urlunparse

import requests
from api4jenkins import Jenkins
from api4jenkins.exceptions import AuthenticationError
from github.CheckRun import CheckRun
from github.Commit import Commit
from github.CommitStatus import CommitStatus
from github.PullRequest import PullRequest
from loguru import logger
from pydantic import BaseModel

from sweepai.config.server import (
    CURL_CA_BUNDLE,
    DEV,
    GITHUB_API_BASE_URL,
    JENKINS_AUTH,
)
from sweepai.core.github_utils import get_token
from sweepai.utils.cache import create_cache
from sweepai.utils.ticket_rendering_utils import (
    hyperlink,
)

logs_cache = create_cache()

### UTILS

# https://docs.github.com/en/rest/checks/runs?apiVersion=2022-11-28#create-a-check-run--parameters
CONCLUSION_TYPES = [
    "action_required",
    "cancelled",
    "failure",
    "neutral",
    "success",
    "skipped",
    "stale",
    "timed_out",
]
STATUS_TYPES = ["completed", "in_progress", "queued", "waiting", "requested", "pending"]
MIN_WAIT_SECONDS = 600  # 10 minutes

RunType = CommitStatus | CheckRun


def create_hyperlink(run: RunType | Commit):
    if isinstance(run, CommitStatus):
        return hyperlink(f"{run.context} - {run.description}", run.target_url)
    elif isinstance(run, CheckRun):
        return hyperlink(f"{run.name} - {run.conclusion}", run.details_url)
    elif isinstance(run, Commit):
        return hyperlink(f"{run.sha[:7]}", run.html_url)
    raise Exception("Invalid run type")


class FixCIInput(BaseModel):
    cleaned_logs: str
    commit_hash: str


def interval_timer(
    total_time: int = 60 * 30,
    interval: int = 5,
):
    for i in range(total_time // interval):
        yield i
        sleep(interval)


### JENKINS LOGS


@lru_cache
def get_jenkins_client(base_url: str):
    if not JENKINS_AUTH:
        return None
    kwargs = (
        {
            "verify": ssl.create_default_context(cafile=CURL_CA_BUNDLE),
            "proxies": {"all://": None},
        }
        if CURL_CA_BUNDLE
        else {}
    )
    for auth in JENKINS_AUTH:
        with suppress(AuthenticationError):
            client = Jenkins(base_url, auth=auth, **kwargs)
            logger.info(client.version)
            break
    else:
        logger.warning("No Jenkins auth provided, skipping Jenkins CI failure check")
        return None
    return client


# E.g. foo » bar » repo » build-pipeline #123
TRIGGERED_BUILDS_PATTERN = r"^(?P<job_name>(.*? » )+)(?P<build_name>.*?) #(?P<build_number>\d+):"


def extract_triggered_builds(build_logs: str) -> list[str]:
    links = []
    sep = " » "
    for match_ in re.finditer(TRIGGERED_BUILDS_PATTERN, build_logs, re.MULTILINE):
        path = match_.group("job_name").strip(sep).split(sep)
        path.append(match_.group("build_name"))
        links.append("/job/" + "/job/".join(path) + "/" + match_.group("build_number"))
    return links


def fetch_jenkins_build_logs(target_url: str):
    parsed_url = urlparse(target_url)
    if not (client := get_jenkins_client(f"{parsed_url.scheme}://{parsed_url.netloc}")):
        logger.warning("No Jenkins auth provided, skipping Jenkins CI failure check")
        return ""
    # Jenkins Python client has bugs
    response = requests.get(target_url.replace("display/redirect", "consoleText"), auth=client._auth)
    try:
        response.raise_for_status()
        original_logs = response.text
        # Sometimes the builds are seed builds that trigger other builds. We search one level deep (no recursion).
        triggered_build_paths = extract_triggered_builds(original_logs)
        for build_path in triggered_build_paths:
            url = urlunparse(
                (
                    parsed_url.scheme,
                    parsed_url.netloc,
                    build_path + "/consoleText",
                    "",
                    "",
                    "",
                )
            )
            response = requests.get(url, auth=client._auth)
            if response.ok:
                original_logs += "\n\n" + response.text
            else:
                logger.error(f"Failed to fetch Jenkins build logs at {build_path}: {response.status_code}")
        return original_logs
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to fetch Jenkins build logs: {e}")
        return ""


### GHA LOGS


def get_run_id(run: CheckRun):
    # E.g. https://github.com/sweepai/sweep-internal/actions/runs/11171470435/job/31056237554
    # PyGithub's "run.id" is actually the job id, run_id is the workflow id, confusing, I know
    _, _, _, _, run_id, *_ = urlparse(run.details_url).path.strip("/").split("/")
    return run_id


def truncate_logs(logs_str: str):
    log_list = logs_str.split("\n")
    truncated_logs = [log[log.find(" ") + 1 :] for log in log_list]
    logs_str = "\n".join(truncated_logs)
    return logs_str


def clean_ansi_logs(logs_str: str) -> str:  # TODO: unit test
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", logs_str)


def format_logs(logs_str: str) -> str:  # TODO: unit test
    return (
        logs_str.replace("##[error]", "\n")
        .replace("##[endgroup]", "\nThe relevant logs are:\n")
        .replace("##[group]", "The command that fails:\n\n")
    )


def post_process_logs(logs_str: str) -> str:  # TODO: unit test
    logs_str = truncate_logs(logs_str)
    logs_str = clean_ansi_logs(logs_str)
    logs_str = format_logs(logs_str)
    return logs_str


def unzip_and_extract_logs(blob: bytes, get_errors_only=True) -> str:
    # Only fetches relevant logs from the zip file
    logs_str = ""
    zip_file = zipfile.ZipFile(io.BytesIO(blob))
    for file in zip_file.namelist():
        if file.endswith(".txt"):
            with zip_file.open(file) as f:
                logs = f.read().decode("utf-8")
                last_line = logs.splitlines()[-1]
                if "##[error]" in last_line:
                    logs_str += logs
                elif not get_errors_only:  # get all logs
                    logs_str += logs
    return logs_str


def download_raw_logs(repo_full_name: str, run_id: str, installation_id: int, get_errors_only=True) -> bytes:
    for _ in range(3):
        # There's actually a hidden redirect here, and it gets automatically handled by the requests library
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {get_token(installation_id=installation_id)}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/repos/{repo_full_name}/actions/runs/{run_id}/logs",
            headers=headers,
        )
        # check for 404
        if response.status_code == 404:
            continue
        return response.content
    raise Exception(f"Failed to download logs for {repo_full_name} run {run_id}")


### ROUTER


def get_ci_failure_logs(installation_id: int, runs: list[RunType], pull_request: PullRequest):
    logs_list = []
    fetched_urls = set()
    for run in runs:
        logger.info(run)
        if isinstance(run, CommitStatus):
            logger.info(f"Run context {run.context}")
            # WARNING: run.target_url might not have jenkins in the url if the organization names it strangely
            # (if so, make this a config) 
            if "jenkins" in run.target_url:  # sometimes it's /pr-head sometimes it's /branch
                # Jenkins format: http://{BASE_URL}/job/{JOB_NAME}/job/PR-{PR_NUMBER}/{RUN_NUMBER}/display/redirect
                if run.target_url not in fetched_urls:
                    logs = fetch_jenkins_build_logs(run.target_url)
                    if logs:
                        logs_list.append(logs)
                        fetched_urls.add(run.target_url)
            # TODO: add support for other CI providers
        elif isinstance(run, CheckRun):
            repo_full_name = pull_request.base.repo.full_name
            actual_run_id = get_run_id(run)
            cache_key = (repo_full_name, actual_run_id, "v3")
            if DEV and (cached_logs := logs_cache.get(cache_key)):
                logs_list.append(cached_logs)
            else:
                raw_binary_logs = download_raw_logs(repo_full_name=repo_full_name, run_id=actual_run_id, installation_id=installation_id)
                raw_logs = unzip_and_extract_logs(raw_binary_logs)
                logs = post_process_logs(raw_logs)
                logs_list.append(logs)
                logs_cache.set(cache_key, logs)
    # TODO: add support for docker runs
    return logs_list


### CI FETCHING LOGIC


def get_ci_failures(pull_request: PullRequest) -> tuple[list[RunType], list[RunType], list[RunType]]:
    commit: Commit = pull_request.get_commits().reversed[0]
    commit_statuses = list(commit.get_statuses())
    pending_statuses = [status for status in commit_statuses if status.state == "pending"]
    successful_statuses = [status for status in commit_statuses if status.state == "success"]
    failing_statuses = [
        status for status in commit_statuses if status.state in ("failure", "error")
    ]  # idfk why github has both failure and error
    check_runs = list(commit.get_check_runs())
    pending_check_runs = [run for run in check_runs if run.status != "completed"]
    successful_check_runs = [run for run in check_runs if run.conclusion == "success"]
    failing_check_runs = [run for run in check_runs if run.conclusion == "failure"]
    return pending_statuses + pending_check_runs, successful_statuses + successful_check_runs, failing_statuses + failing_check_runs


def wait_for_ci_failures(pull_request: PullRequest) -> tuple[list[RunType], list[RunType], list[RunType]]:
    # can use async
    pending_runs = []
    successful_runs = []
    error_runs = []
    for i in interval_timer():
        pending_runs, successful_runs, error_runs = get_ci_failures(pull_request)

        if error_runs:
            break
        elif not pending_runs and i > MIN_WAIT_SECONDS // 5:
            return [], [], []
        else:
            logger.debug(f"Pending runs: {pending_runs}")
            logger.debug(f"Successful runs: {successful_runs}")
            logger.debug(f"PR URL: {pull_request.html_url}")
    return pending_runs, successful_runs, error_runs
