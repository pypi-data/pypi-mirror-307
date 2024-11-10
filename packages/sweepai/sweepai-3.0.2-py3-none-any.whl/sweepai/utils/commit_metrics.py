import os
import re
from datetime import datetime, timezone
from typing import Iterator

from diskcache import Cache
from github import Github, UnknownObjectException
from github.PullRequestComment import PullRequestComment
from github.GithubObject import NotSet
from github.Issue import Issue
from github.Repository import Repository
from loguru import logger
from tqdm import tqdm

from sweepai.config.server import (
    CACHE_DIRECTORY,
    GITHUB_API_BASE_URL,
    GITHUB_BASE_URL,
    GITHUB_BOT_USERNAME,
)
from sweepai.core.github_links import CommentURL, IssueURL, parse_url
from sweepai.core.github_utils import REPO_CACHE_BASE_DIR, github_integration
from sweepai.utils.str_utils import ordered_dedup

METRICS_FILE = f"{CACHE_DIRECTORY}/metrics.csv"

metrics_cache = Cache(f"{CACHE_DIRECTORY}/metrics_cache")

metrics_cutoff_date = datetime(2024, 8, 1)

# TODO: this type of mapping exists elsewhere
FILE_EXTENSION_TO_LANGUAGE = {
    # Programming languages
    "py": "python",
    "ts": "typescript",
    "tsx": "typescript",
    "js": "javascript",
    "jsx": "javascript",
    "cpp": "cpp",
    "c": "c",
    "h": "c",
    "hpp": "cpp",
    "java": "java",
    "rb": "ruby",
    "php": "php",
    "go": "go",
    "rs": "rust",
    "swift": "swift",
    "kt": "kotlin",
    "scala": "scala",
    "cs": "csharp",
    "fs": "fsharp",
    "vb": "visualbasic",
    # Markup and data formats
    "md": "markdown",
    "txt": "plaintext",
    "yml": "yaml",
    "yaml": "yaml",
    "json": "json",
    "xml": "xml",
    "html": "html",
    "css": "css",
    "scss": "scss",
    "less": "less",
    # Configuration files
    "ini": "ini",
    "cfg": "config",
    "conf": "config",
    "toml": "toml",
    # Shell scripts
    "sh": "shell",
    "bash": "shell",
    "zsh": "shell",
    "bat": "batch",
    "ps1": "powershell",
    # Other
    "sql": "sql",
    "r": "r",
    "dockerfile": "dockerfile",
    "gitignore": "gitignore",
    "csv": "csv",
    "log": "log",
}


def make_aware(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# def get_bot_username():
#     return GITHUB_BOT_USERNAME.rstrip("[bot]") + "[bot]"


def extract_pr_url(content):
    pattern = r"https://.*?/pull/\d+"
    match = re.search(pattern, content, re.IGNORECASE)
    if match:
        return match.group(0)
    return None


def get_pr_links_from_issue(issue: Issue):
    """Works for issues that are labeled with sweep"""
    pr_links = []
    if issue.pull_request is None:
        comments = issue.get_comments()
        for comment in comments:
            if comment.user.login == GITHUB_BOT_USERNAME:
                pr_link = extract_pr_url(comment.body)
                if pr_link:
                    logger.info(f"Pull request URL found: {pr_link}")
                    pr_links.append(pr_link)
    return pr_links


def extract_issue_or_comment_url(content):
    # Try to find a link
    pattern = rf"https://{GITHUB_BASE_URL}.*?/(issues/\d+(#issuecomment-\d+)?|pull/\d+(#issuecomment-\d+|#discussion_r\d+|#r\d+))"
    match = re.search(pattern, content, re.IGNORECASE)
    if match:
        return match.group(0)
    return None


def get_issue_or_comment_link_from_pr(issue):
    if issue.pull_request is not None:
        issue_or_comment_link = extract_issue_or_comment_url(issue.body)
        if issue_or_comment_link:
            return issue_or_comment_link
    return None


def extract_issue_number_from_pr_body(content):
    pattern = r"Fixes(?:\s)*#(\d+)"
    match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1)
    return None


def get_issue_link_from_pr_body(issue, repo):
    if issue.pull_request is not None:
        issue_number = extract_issue_number_from_pr_body(issue.body)
        if issue_number:
            issue = repo.get_issue(int(issue_number))
            return issue.html_url
    return None


def get_timestamp_of_last_label(issue: Issue):
    paginated_list = issue.get_timeline().reversed
    paginated_list.per_page = 100
    for event in paginated_list:
        if event.event == "labeled" and event.raw_data.get("label", {}).get("name") == "sweep":
            return make_aware(event.created_at)
    return datetime.fromtimestamp(0, tz=timezone.utc)  # same type, but 0 to indicate something is wrong


def get_original_issues_from_pr_link(
    g: Github, repo_name: str, ignore_cache: bool = False
) -> dict[str, (str, str, str, str)]:
    """Returns a dict where key is the pr_link and value is a tuple of (issue_link, issue_author, issue_title, issue.created_at)"""
    key = ("original_issues", repo_name, "v1")
    if key in metrics_cache and not ignore_cache:
        return metrics_cache.get(key)

    result = {}
    try:
        # Get the repository
        repo = g.get_repo(repo_name)
    except Exception as e:
        logger.error(f"Error accessing repository: {e}")
        return result

    try:
        key = ("issues_with_sweep_label", repo_name, "v0")
        if key not in metrics_cache or ignore_cache:
            issues_with_sweep_label: list[Issue] = ordered_dedup(
                list(
                    repo.get_issues(
                        labels=["sweep"],
                        state="all",
                        sort="created",
                        direction="desc",
                        since=metrics_cutoff_date,
                    )
                )
                + list(
                    repo.get_issues(
                        creator=f"{GITHUB_BOT_USERNAME}",
                        state="all",
                        sort="created",
                        direction="desc",
                        since=metrics_cutoff_date,
                    )
                )
            )
            metrics_cache.set(key, issues_with_sweep_label)
        else:
            issues_with_sweep_label: list[Issue] = metrics_cache.get(key)
        for issue in issues_with_sweep_label:
            logger.info(
                f"Issue #{issue.number}: {issue.title} Issue Author: {issue.user.login} Issue Updated At: {issue.created_at}"
            )
            pr_links = get_pr_links_from_issue(issue)
            logger.info(f"PR Links: {pr_links}")
            for pr_link in pr_links:
                if pr_link not in result:  # might want the latest here
                    result[pr_link] = (
                        issue.html_url,
                        issue.user.login,
                        issue.title,
                        issue.created_at,
                        get_timestamp_of_last_label(issue),
                    )
    except Exception as e:
        logger.error(f"Error accessing issues for repository {repo_name}: {e}")
        return result
    metrics_cache.set(key, result)
    return result


def retrieve_link_data(repo: Repository, issue_link: str):
    parsed_url = parse_url(issue_link)
    logger.debug(f"Issue link: {issue_link}")
    match parsed_url:
        case CommentURL(
            pull_request_number=issue_number,
            comment_id=comment_number,
            is_review_comment=is_review_comment,
        ):
            logger.debug(f"Issue comment")
            logger.debug(f"Issue number: {issue_number}")
            logger.debug(f"Issue comment number: {comment_number}")
            referenced_pr = repo.get_pull(int(issue_number))
            if is_review_comment:
                comment = referenced_pr.get_comment(int(comment_number))
            else:
                referenced_pr = referenced_pr.as_issue()
                comment = referenced_pr.get_comment(int(comment_number))
            issue_author = comment.user.login
            issue_title = comment.body
            issue_created_at = comment.created_at
            issue_labelled_at = issue_created_at
        case IssueURL(issue_number=issue_number):
            logger.debug(f"Issue")
            referenced_issue = repo.get_issue(issue_number)
            issue_author = referenced_issue.user.login
            issue_title = referenced_issue.title
            issue_created_at = referenced_issue.created_at
            issue_labelled_at = get_timestamp_of_last_label(referenced_issue)
        case _:
            raise ValueError(f"Invalid issue link: {issue_link}")
    return issue_author, issue_title, issue_created_at, issue_labelled_at

# Comment Extraction

def get_sweep_bot_comments(repo: Repository) -> Iterator[PullRequestComment]:
    repo._requester.per_page = 100
    comments = repo.get_issues_comments(
        sort="created",
        direction="desc",
        since=datetime(2024, 10, 15),
    )
    for comment in list(tqdm(comments)):
        if not hasattr(comment, "pull_request_url"): # only get PR comments
            continue
        body = comment.body
        if "Hey, @" in body and "I finished working on this. Here are the changes I made:" in body:
            yield comment

def extract_commit_sha_from_sweep_bot_comment(body: str) -> str | None:
    # E.g. 🔄 Revert 91fcee84c37da688a368cbb3a9b47acd9eb3e22e?
    pattern = r"Revert (?P<sha>\w{40})\?"
    match = re.search(pattern, body)
    if match:
        return match.group("sha")
    return None

def extract_username_from_sweep_bot_comment(body: str) -> str | None:
    # E.g. Hey, @username, I finished working on this. Here are the changes I made:
    pattern = r"Hey, @(?P<username>.+), I finished working on this. Here are the changes I made:"
    match = re.search(pattern, body)
    if match:
        return match.group("username")
    return None

def get_commit_metrics_repo(
    g: Github,
    repo_name: str,
    start_date: datetime | type[NotSet] | None = NotSet,
    ignore_cache: bool = False,
):
    all_commit_data_key = ("all_commit_data", repo_name, "v1")
    if all_commit_data_key in metrics_cache and not ignore_cache:
        return metrics_cache.get(all_commit_data_key)

    try:
        # Get the repository
        repo = g.get_repo(repo_name)
        repo._requester.per_page = 100 # sets pagination to 100
    except Exception as e:
        logger.error(f"Error accessing repository: {e}")
        return []

    # Retrieve PRs since the specified start date
    try:
        issues_created_by_sweep = list(
            repo.get_issues(
                creator=f"{GITHUB_BOT_USERNAME}",
                state="all",
                sort="created",
                direction="desc",
                since=start_date,
            )
        )
    except Exception as e:
        logger.error(f"Error accessing issues for repository {repo_name}: {e}")
        return []

    commit_data = []
    commit_unique_ids = set()
    for pr in issues_created_by_sweep:
        logger.info(f"PR: {pr.html_url}")

        # get the data for the pull request
        if pr.pull_request is None:
            continue
        pull_request_html_url = pr.pull_request.html_url
        pull_request_number = pull_request_html_url.split("/")[-1]
        if not pull_request_number.isdigit():
            continue
        try:
            pull_request = repo.get_pull(int(pull_request_number))
        except Exception as e:
            logger.error(f"Error accessing pull request {pull_request_number} for repository {repo_name}: {e}")
            continue

        # get the commits for the pull request
        try:
            commits = list(pull_request.get_commits())
        except Exception as e:
            logger.error(
                f"Error accessing commits for pull request {pull_request_number} for repository {repo_name}: {e}"
            )
            continue

        is_merged = pull_request.merged
        merged_by = pull_request.merged_by
        if is_merged and merged_by is not None and "sweep" in merged_by.login.lower():
            logger.info(f"Pull request {pull_request_html_url} was merged by Sweep")
            continue

        # get the issue link from the pull request
        issue_link = get_issue_or_comment_link_from_pr(pr)
        if issue_link is None:
            issue_link = get_issue_link_from_pr_body(pr, repo)
        logger.info(f"Issue Link: {issue_link}")

        if issue_link is None:
            issue_link = "N/A"
            issue_author = "N/A"
            issue_title = "N/A"
            issue_created_at = "N/A"
            issue_labelled_at = "N/A"
        else:
            issue_author, issue_title, issue_created_at, issue_labelled_at = retrieve_link_data(repo, issue_link)

        for commit in commits:
            logger.info(f"Commit: {commit.sha}")
            sha = commit.sha

            # Get the author's username
            author = commit.author.login if commit.author else commit.commit.author.name
            date = commit.commit.author.date

            try:
                # Access the files changed in the commit
                files = list(commit.files)
            except Exception as e:
                logger.error(f"Error accessing files for commit {sha}: {e}")
                continue

            for file in files:
                # Create a unique ID based on SHA and file path
                unique_id = f"{sha}_{file.filename}"
                if unique_id in commit_unique_ids:
                    continue
                commit_unique_ids.add(unique_id)

                additions = file.additions
                deletions = file.deletions

                # Detect the language by examining the file content
                file_extension = file.filename.split(".")[-1]
                language = FILE_EXTENSION_TO_LANGUAGE.get(file_extension, file_extension)

                new_commit_data = {
                    "id": unique_id,
                    "sha": sha,
                    "file_name": file.filename,
                    "org_name": repo.owner.login,
                    "repo_name": repo.name,
                    "author": author,
                    "date": date,
                    "additions": additions,
                    "deletions": deletions,
                    "language": language,
                    "pr_number": pr.number,
                    "pr_state": pr.state,
                    "pr_link": pull_request_html_url,
                    "pr_is_merged": is_merged,
                    "pr_created_at": pr.created_at,
                    "issue_link": issue_link,
                    "issue_author": issue_author,
                    "issue_title": issue_title,
                    "issue_created_at": issue_created_at,
                    "issue_labelled_at": issue_labelled_at,
                }
                metrics_cache.set(("commit_data", unique_id), new_commit_data)
                commit_data.append(new_commit_data)
    
    for comment in get_sweep_bot_comments(repo):
        body = comment.body
        commit_sha = extract_commit_sha_from_sweep_bot_comment(body)
        if commit_sha is None:
            continue
        username = extract_username_from_sweep_bot_comment(body)
        if username is None:
            continue
        try:
            # Access the files changed in the commit
            commit = repo.get_commit(commit_sha)
            files = list(commit.files)
        except Exception as e:
            logger.error(f"Error accessing files for commit {sha}: {e}")
            continue

        pr_number = comment.pull_request_url.split("/")[-1]

        for file in files:
            file_extension = file.filename.split(".")[-1]
            commit_data.append({
                "id": f"{commit_sha}_comment",
                "sha": commit_sha,
                "file_name": file.filename,
                "org_name": repo.owner.login,
                "repo_name": repo.name,
                "author": username,
                "date": comment.updated_at,
                "additions": file.additions,
                "deletions": file.deletions,
                "language": FILE_EXTENSION_TO_LANGUAGE.get(file_extension, file_extension),
                "pr_number": pr_number,
                "pr_state": "N/A",
                "pr_link": "N/A",
                "pr_is_merged": True,
                "pr_created_at": commit.commit.author.date,
                "issue_link": comment.html_url, # TODO: Add original issue link
                "issue_author": username,
                "issue_title": "N/A", # TODO: extract from blockquote
                "issue_created_at": comment.created_at, # these are approximations
                "issue_labelled_at": comment.created_at,
            })

    metrics_cache.set(all_commit_data_key, commit_data)
    return commit_data


def list_git_dirs(REPO_CACHE_BASE_DIR):
    paths = []

    def has_git_in_base(dir_path):
        base_dir = os.path.join(dir_path, "base")
        if os.path.isdir(base_dir):
            for dirname in os.listdir(base_dir):
                dirpath = os.path.join(base_dir, dirname)
                git_dir = os.path.join(dirpath, ".git")
                if os.path.isdir(git_dir):
                    return True
        return False

    for child in os.listdir(REPO_CACHE_BASE_DIR):
        child_path = os.path.join(REPO_CACHE_BASE_DIR, child)
        if os.path.isdir(child_path):
            # Check if child_path/base/ANYDIRNAME/.git exists
            if has_git_in_base(child_path):
                relative_path = os.path.relpath(child_path, REPO_CACHE_BASE_DIR)
                paths.append(relative_path)
            # Check for grandchild directories
            for grandchild in os.listdir(child_path):
                grandchild_path = os.path.join(child_path, grandchild)
                if os.path.isdir(grandchild_path):
                    # Check if grandchild_path/base/ANYDIRNAME/.git exists
                    if has_git_in_base(grandchild_path):
                        relative_path = os.path.relpath(grandchild_path, REPO_CACHE_BASE_DIR)
                        paths.append(relative_path)
    return paths


def get_commit_metrics(access_token: str = None, ignore_cache: bool = False) -> list[dict]:
    if not access_token:
        logger.info("Access token not provided. Using unauthenticated GitHub API.")
    repo_names = list_git_dirs(REPO_CACHE_BASE_DIR)
    commit_data = []

    g = Github(access_token, base_url=GITHUB_API_BASE_URL) if access_token else None

    for repo_full_name in tqdm(repo_names, desc="Processing repositories"):
        if (current_g := g) is None:
            org_name, repo_name = repo_full_name.split("/")
            try:
                installation = github_integration.get_repo_installation(owner=org_name, repo=repo_name)
            except UnknownObjectException as e:
                logger.error(f"Error accessing installation for repository {repo_full_name}: {e}")
                continue
            current_g = installation.get_github_for_installation()

        if commit_data_repo := get_commit_metrics_repo(current_g, repo_full_name, metrics_cutoff_date, ignore_cache):
            commit_data.extend(commit_data_repo)
            logger.info(f"Commit data for repository {repo_full_name}: {len(commit_data_repo)} commits")
    convert_metrics_to_csv(commit_data)
    return commit_data


def convert_metrics_to_csv(commit_data: list[dict]):
    import pandas as pd

    df = pd.DataFrame(commit_data)
    if len(df) == 0:
        print("No commit data to convert to CSV")
        return

    # Check for required columns and add them with default values if missing
    required_columns = [
        "pr_link",
        "pr_number",
        "pr_state",
        "pr_is_merged",
        "pr_created_at",
        "issue_link",
        "issue_author",
        "issue_title",
        "issue_created_at",
        "issue_labelled_at",
        "file_name",
        "language",
        "additions",
        "deletions",
        "author",
        "date",
        "repo_name",
        "org_name",
    ]

    for column in required_columns:
        if column not in df.columns:
            print(f"Column '{column}' is missing. Adding it with default value 'N/A'")
            df[column] = "N/A"

    # Convert 'date' column to datetime if it's not already
    if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    def process_group(group):
        num_files = group["file_name"].nunique()
        group["total_changes"] = group["additions"] + group["deletions"]

        # language with most number of additions + deletions
        language_totals = group.groupby("language")["total_changes"].sum()
        primary_language = language_totals.idxmax()

        # list of other languages
        all_languages = group["language"].unique().tolist()
        all_languages_str = ";".join(all_languages)

        authors = group["author"].dropna().unique()
        authors_str = ";".join(authors)

        # For other columns, take the first value
        first_row = group.iloc[0]

        if first_row["issue_labelled_at"] is None or first_row["issue_created_at"] == "N/A":
            issue_to_pr_time_in_seconds = "N/A"
        else:
            issue_to_pr_time_in_seconds = (first_row["pr_created_at"] - first_row["issue_labelled_at"]).total_seconds()

        return pd.Series(
            {
                "pr_number": first_row["pr_number"],
                "pr_state": first_row["pr_state"],
                "pr_link": first_row["pr_link"],
                "pr_is_merged": any(group["pr_is_merged"]),
                "pr_created_at": first_row["pr_created_at"],
                "issue_link": first_row["issue_link"],
                "issue_author": first_row["issue_author"],
                "issue_title": first_row["issue_title"],
                "issue_created_at": first_row["issue_created_at"],
                "issue_labelled_at": first_row["issue_labelled_at"],
                "issue_creation_seconds": issue_to_pr_time_in_seconds,
                "num_files": num_files,
                "total_lines_changed": group["total_changes"].sum(),
                "primary_language": primary_language,
                "all_languages": all_languages_str,
                "authors": authors_str,
                "repo_name": first_row["repo_name"],
                "org_name": first_row["org_name"],
            }
        )

    try:
        grouped = df.groupby("pr_link")[required_columns].apply(process_group).reset_index(drop=True)
        logger.info(f"Writing metrics to {METRICS_FILE}")
        grouped.to_csv(METRICS_FILE, index=False)
        logger.info(f"Metrics successfully written to {METRICS_FILE}")
    except Exception as e:
        logger.exception(f"Error in grouping or writing CSV: {str(e)}")
        logger.error("Columns in DataFrame: " + ", ".join(df.columns))


if __name__ == "__main__":
    commit_data = get_commit_metrics(None, ignore_cache=True)
    logger.info(f"Commit data: {commit_data}")
