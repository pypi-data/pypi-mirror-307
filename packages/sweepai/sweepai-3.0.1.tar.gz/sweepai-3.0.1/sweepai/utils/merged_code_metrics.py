"""
This script is used to compute metrics for merged code suggestions. It is used to determine the percentage of lines added in a PR that were suggested by Sweep.
"""

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from random import randint

from diskcache import Cache
from github.Repository import Repository
from loguru import logger

from sweepai.backend.api_utils import (
    get_cached_installation_id,
    get_github_client_from_org,
)
from sweepai.config.server import CACHE_DIRECTORY
from sweepai.core.github_utils import ClonedRepo
from sweepai.utils.diff import generate_diff
from sweepai.utils.str_utils import strip_triple_quotes

metrics_cache = Cache(f"{CACHE_DIRECTORY}/metrics_cache")

TWENTY_FOUR_HOURS = 24 * 60 * 60
SIX_HOURS = 6 * 60 * 60
CACHE_VERSION = "0.0.1"
EMPTY_METRIC_PLACEHOLDER = "EMPTY_CACHE_VALUE"


# can be reworked later for actual display, this will do for now
def get_highlighted_lines(lines: list[str], common_lines: list[str]) -> str:
    formatted_lines = []
    for line in lines:
        if line in common_lines:
            formatted_lines.append(f"\033[94m{line}\033[0m")  # Blue color
        else:
            formatted_lines.append(line)
    return "\n".join(formatted_lines)


def get_pr_for_branch(repo: Repository, org_name: str, branch: str):
    pull_requests = repo.get_pulls(state="closed", head=f"{org_name}:{branch}")
    max_prs = 2
    for idx, pr in enumerate(pull_requests):
        if idx >= max_prs:
            break
        logger.info(pr.head.ref)
        if pr.head.ref == branch and pr.merged:
            return pr.html_url, {file.filename: file.patch for file in pr.get_files()}
    return None, {}


def get_sweep_code_suggestions(all_messages_joined):
    pattern = r"<code_change>\s*<file_path>\n*(?P<filePath>[\s\S]+?)\n*</file_path>\s*(<justification>\n*(?P<justification>[\s\S]+?)\n*</justification>)?\s*(<original_code>\n*(?P<originalCode>[\s\S]*?)</original_code>\n*)?<new_code>\n*(?P<newCode>[\s\S]+?)\n*(</new_code>)?\s*</code_change>"
    sweep_code_suggestions = [
        {
            "filePath": match_.groupdict().get("filePath", ""),
            "originalCode": strip_triple_quotes(match_.groupdict().get("originalCode") or ""),
            "newCode": strip_triple_quotes(match_.groupdict().get("newCode") or ""),
        }
        for match_ in re.finditer(pattern, all_messages_joined, re.DOTALL)
    ]
    return sweep_code_suggestions


def extract_changed_lines(diff):
    changed_lines = []
    for line in diff.split("\n"):
        # added line
        if line.startswith("+") and not line.startswith("+++"):
            changed_lines.append(line[1:])
        # removed line
        elif line.startswith("-") and not line.startswith("---"):
            changed_lines.append(line[1:])
    return changed_lines


def find_common_lines(changes_dict: dict[str, list[str]], second_list: list[str]) -> list[str]:
    stripped_second_list = [line.strip() for line in second_list]
    common_lines = []
    for _, changed_lines in changes_dict.items():
        for line in changed_lines:
            if line.strip() in stripped_second_list:
                common_lines.append(line)
    return common_lines


@dataclass
class Metrics:
    percentage_of_lines_added: float
    number_of_lines_added: int
    highlighted_lines: str
    common_added_lines: list[str]
    pull_request_url: str
    message_id: str
    last_modified_date: str
    org_name: str
    repo_name: str
    username: str


def compute_metrics(
    sweep_code_suggestions,
    file_patches: dict[str, str],
    metadata: dict,
    latest_cloned_repos: dict[str, ClonedRepo] = {},
) -> Metrics:
    generated_diffs = [
        (
            suggestion["filePath"],
            generate_diff(suggestion["originalCode"], suggestion["newCode"], n=0),
        )
        for suggestion in sweep_code_suggestions
    ]
    sweep_suggested_changed_lines = {}
    for file_path, diff in generated_diffs:
        sweep_suggested_changed_lines[file_path] = extract_changed_lines(diff)

    pr_changed_lines = []
    common_added_lines = []
    # this checks if the PR already exists
    if metadata["did_pr_exist"]:
        for patch in file_patches.values():
            pr_changed_lines.extend(extract_changed_lines(patch))
        common_added_lines = find_common_lines(sweep_suggested_changed_lines, pr_changed_lines)
    else:
        # check the file in the cloned repo and then see if the sweep's suggestion exists in the file
        cloned_repo = get_cloned_repo(
            repo_full_name=metadata["repo_full_name"],
            latest_cloned_repos=latest_cloned_repos,
        )
        for file_path, changed_lines in sweep_suggested_changed_lines.items():
            try:
                file_contents = cloned_repo.get_file_contents(file_path)
                for line in changed_lines:
                    if line in file_contents:
                        common_added_lines.append(line)
            except FileNotFoundError:
                logger.warning(f"File not found (likely renamed):")
    number_of_lines_added = len(common_added_lines)
    total_pr_lines = max(len(pr_changed_lines), 1)  # Avoid division by zero
    percentage_of_lines_added = 0 if total_pr_lines <= 1 else int((number_of_lines_added / total_pr_lines) * 100)
    pull_request_url = metadata["pull_request_url"] if metadata["did_pr_exist"] else "N/A"

    org_name, repo_name = metadata["repo_full_name"].split("/")

    return Metrics(
        percentage_of_lines_added=percentage_of_lines_added,
        number_of_lines_added=number_of_lines_added,
        highlighted_lines=get_highlighted_lines(pr_changed_lines, common_added_lines),
        common_added_lines=common_added_lines,
        pull_request_url=pull_request_url,
        message_id=metadata["message_id"],
        last_modified_date=metadata["last_modified_date"],
        org_name=org_name,
        repo_name=repo_name,
        username=metadata["username"],
    )


def get_data_from_json_path(json_path: str):
    data = {}
    try:
        # get the last time the file was modified
        with open(json_path, "r") as file:
            data = json.load(file)
        last_modified = os.path.getmtime(json_path)
        data["last_modified"] = last_modified
    except Exception as e:
        logger.error(f"Error loading json file: {e}")
    return data


def get_pr_and_file_patches(data: dict) -> tuple[str, dict[str, str], bool]:
    branch = data["branch"]
    repo_full_name = data["repo_name"]
    pr_cache_key = f"pr-{repo_full_name}-{branch}-v{CACHE_VERSION}"
    pr_cache_hit = metrics_cache.get(pr_cache_key)
    if pr_cache_hit:
        return pr_cache_hit
    org_name = repo_full_name.split("/")[0] if "/" in repo_full_name else None
    if not org_name:
        raise ValueError(f"Could not determine org name from repo name: {repo_full_name}")
    try:
        _, github_client = get_github_client_from_org(org_name)
    except Exception:
        raise Exception(f"Error getting github client for {repo_full_name}")
    repo = github_client.get_repo(repo_full_name)
    pull_request_url, file_patches = get_pr_for_branch(repo=repo, org_name=org_name, branch=branch)
    if pull_request_url:
        metrics_cache.set(
            pr_cache_key, (pull_request_url, file_patches, True)
        )  # if a pr exists, cache it with no expiration
    did_pr_exist = pull_request_url is not None
    return pull_request_url, file_patches, did_pr_exist


def get_metrics_for_json_path(json_path: str, latest_cloned_repos: dict[str, ClonedRepo] = {}):
    """This file is the topmost cache layer for metrics. It will check if the metrics are already cached and return them if they are. If not, it will compute the metrics and cache them."""
    cache_key = f"metrics-{json_path}-v{CACHE_VERSION}"
    metrics_cache_hit = metrics_cache.get(cache_key)
    if metrics_cache_hit and metrics_cache_hit != EMPTY_METRIC_PLACEHOLDER:
        return metrics_cache_hit
    try:
        data = get_data_from_json_path(json_path=json_path)
        all_messages_joined = "\n\n".join([message["content"] for message in data["messages"]])
        sweep_code_suggestions = get_sweep_code_suggestions(all_messages_joined)
        pull_request_url, file_patches, did_pr_exist = get_pr_and_file_patches(data)
        pull_request_url = pull_request_url or "N/A"
        message_id = ""
        if json_path and "/" in json_path:
            message_id = json_path.split("/")[-1].replace(".json", "")
        metadata = {
            "pull_request_url": pull_request_url,
            "message_id": message_id,
            "last_modified_date": datetime.fromtimestamp(data["last_modified"]).strftime("%Y-%m-%d %H:%M:%S"),
            "repo_full_name": data["repo_name"],
            "did_pr_exist": did_pr_exist,
            "username": data["username"],
        }
        # all computation happens in compute_metrics
        computed_metrics = compute_metrics(
            sweep_code_suggestions=sweep_code_suggestions,
            file_patches=file_patches,
            metadata=metadata,
            latest_cloned_repos=latest_cloned_repos,
        )
        if computed_metrics.number_of_lines_added > 0 or did_pr_exist:
            metrics_cache.set(cache_key, computed_metrics)  # This does not expire
        return computed_metrics
    except Exception as e:
        logger.warning(f"Error computing metrics for {json_path}: {e}")
        metrics_cache.set(
            cache_key, EMPTY_METRIC_PLACEHOLDER, expire=SIX_HOURS * randint(1, 5)
        )  # add jitter to avoid cache stampede
        return EMPTY_METRIC_PLACEHOLDER


def get_cloned_repo(repo_full_name: str, latest_cloned_repos: dict[str, ClonedRepo]):
    if repo_full_name in latest_cloned_repos:
        return latest_cloned_repos[repo_full_name]
    org_name = repo_full_name.split("/")[0]
    try:
        installation_id = get_cached_installation_id(org_name)
    except Exception as e:
        raise Exception(f"Error getting installation id for {org_name}: {e}")
    cloned_repo = ClonedRepo(repo_full_name=repo_full_name, installation_id=installation_id)
    latest_cloned_repos[repo_full_name] = cloned_repo
    return cloned_repo


def compute_metrics_for_all_messages(csv_file: str):
    logger.info(f"Computing metrics for all messages")
    # sort the jsons by last updated first
    all_message_jsons = [
        (
            f"{CACHE_DIRECTORY}/messages/{file}",
            os.path.getmtime(f"{CACHE_DIRECTORY}/messages/{file}"),
        )
        for file in os.listdir(f"{CACHE_DIRECTORY}/messages")
        if file.endswith(".json")
    ]
    all_message_jsons = [file for file, _ in sorted(all_message_jsons, key=lambda x: x[1], reverse=True)]
    # make this sequential to be less costly + to allow safe sharing of cloned repos dictionary
    latest_cloned_repos = {}
    all_metrics = []
    for json_path in all_message_jsons:
        metrics = get_metrics_for_json_path(json_path, latest_cloned_repos)
        if metrics != EMPTY_METRIC_PLACEHOLDER and metrics is not None:
            all_metrics.append(
                {
                    "last_modified_date": metrics.last_modified_date,
                    "message_link": metrics.message_id,
                    "number_of_pr_lines_merged": metrics.number_of_lines_added,
                    "percentage_of_pr_lines_merged": metrics.percentage_of_lines_added,
                    "pull_request_url": metrics.pull_request_url,
                    "org_name": metrics.org_name,
                    "repo_name": metrics.repo_name,
                    "username": metrics.username,
                }
            )
    total_messages = len(all_message_jsons)
    successful_messages_counted = len(all_metrics)

    # Calculate sessions per day
    sessions_per_day = {}
    for metric in all_metrics:
        date = metric["last_modified_date"].split()[0]  # Extract date part
        sessions_per_day[date] = sessions_per_day.get(date, 0) + 1

    # Update all_metrics with sessions count; we turned off message forking so this is 1:1
    for metric in all_metrics:
        date = metric["last_modified_date"].split()[0]
        metric["sessions_count"] = sessions_per_day[date]
    from pandas import DataFrame

    df = DataFrame(all_metrics)
    # Dedupe rows, keeping the one with the greatest number of lines changed for a given PR URL
    df = df.sort_values("number_of_pr_lines_merged", ascending=False).drop_duplicates(
        subset="pull_request_url", keep="first"
    )
    df.sort_values(by="last_modified_date", inplace=True)
    df.to_csv(csv_file, index=False, na_rep="N/A")
    logger.info(
        f"Metrics written to {csv_file}\n{successful_messages_counted}/{total_messages} messages, {round((successful_messages_counted / total_messages) * 100, 1)}% successfully computed"
    )
    return all_metrics


if __name__ == "__main__":
    csv_file = f"{CACHE_DIRECTORY}/metrics.csv"
    all_metrics = compute_metrics_for_all_messages(csv_file=csv_file)
