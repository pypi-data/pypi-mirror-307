"""
on_ticket is the main function that is called when a new issue is created.
It is only called by the webhook handler in sweepai/api.py.
"""

import hashlib
import io
import os
import re
import traceback
import zipfile
from bdb import BdbQuit
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain
from typing import Callable

import requests
from github import IncompletableObject
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from loguru import logger

from sweepai.config.client import SweepConfig
from sweepai.config.server import DOCUMENTATION_URL
from sweepai.core.github_utils import get_token
from sweepai.dataclasses.codereview import CodeReview, CodeReviewIssue
from sweepai.handlers.on_check_suite import clean_gh_logs, remove_ansi_tags
from sweepai.utils.str_utils import sanitize_string_for_github

MESSAGE_MARKER = "\n\n<!--- MESSAGE_MARKER --->"
PR_REVERT_BUTTON = "- [ ] Revert"
PR_REVERTED_INDICATOR = "- [x] Revert"
DOCUMENTATION_STRING = (
    f"\n\n:book: For more information on how to use Sweep, please read our [documentation]({DOCUMENTATION_URL})."
)

sweeping_png = """<a href="https://sweep.dev"><img src="https://raw.githubusercontent.com/sweepai/sweep/main/.assets/sweep-square.png" width="100" style="width:50px; margin-bottom:10px" alt="Sweeping"></a>"""

INSTRUCTIONS_FOR_REVIEW = """\
### 💡 To get Sweep to edit this pull request, you can:
* Comment below, and Sweep can edit the entire PR
* Comment on a file, Sweep will only modify the commented file
* Edit the original issue to get Sweep to recreate the PR from scratch"""

SWEEP_PR_REVIEW_HEADER = "# Sweep: PR Review"

HR = "\n\n---\n\n"

OVERRIDE_ISSUE_VALIDATION = "OVERRIDE_ISSUE_VALIDATION"


def center(text: str) -> str:
    return f"<div align='center'>{text}</div>"


SWEEPING_PNG = f"{center(sweeping_png)}\n\n"


def hyperlink(text: str, url: str) -> str:
    return f"[{text}]({url})"


# Add :eyes: emoji to ticket
def add_emoji(issue: Issue, comment_id: int = None, reaction_content="eyes"):
    item_to_react_to = issue.get_comment(comment_id) if comment_id else issue
    item_to_react_to.create_reaction(reaction_content)


# Add :eyes: emoji to ticket
def add_emoji_to_pr(pr: PullRequest, comment_id: int = None, reaction_content="eyes"):
    item_to_react_to = pr.get_comment(comment_id) if comment_id else pr
    item_to_react_to.create_reaction(reaction_content)


# takes in a list of workflow runs and returns a list of messages containing the logs of the failing runs
def get_failing_gha_logs(runs, installation_id) -> str:
    token = get_token(installation_id)
    all_logs = ""
    for run in runs:
        # jobs_url
        jobs_url = run.jobs_url
        jobs_response = requests.get(
            jobs_url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        if jobs_response.status_code == 200:
            failed_jobs = []
            jobs = jobs_response.json()["jobs"]
            for job in jobs:
                if job["conclusion"] == "failure":
                    failed_jobs.append(job)

            failed_jobs_name_list = []
            for job in failed_jobs:
                # add failed steps
                for step in job["steps"]:
                    if step["conclusion"] == "failure":
                        parsed_name = step["name"].replace("/", "")
                        failed_jobs_name_list.append(f"{job['name']}/{step['number']}_{parsed_name}")
        else:
            logger.error("Failed to get jobs for failing github actions, possible a credentials issue")
            return all_logs
        # make sure jobs in valid
        if jobs_response.json()["total_count"] == 0:
            logger.warning(f"no jobs for this run: {run}, continuing...")
            continue

        # logs url
        logs_url = run.logs_url
        logs_response = requests.get(
            logs_url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            allow_redirects=True,
        )
        # Check if the request was successful
        if logs_response.status_code == 200:
            zip_data = io.BytesIO(logs_response.content)
            zip_file = zipfile.ZipFile(zip_data, "r")
            zip_file_names = zip_file.namelist()
            for file in failed_jobs_name_list:
                if f"{file}.txt" in zip_file_names:
                    logs = zip_file.read(f"{file}.txt").decode("utf-8")
                    logs_prompt = clean_gh_logs(logs)
                    all_logs += logs_prompt + "\n"
        else:
            logger.error("Failed to get logs for failing github actions, likely a credentials issue")
    return remove_ansi_tags(all_logs)


def get_branch_diff_text(repo, branch, base_branch=None):
    base_branch = base_branch or SweepConfig.get_branch(repo)
    comparison = repo.compare(base_branch, branch)
    file_diffs = comparison.files

    priorities = {
        "added": 0,
        "renamed": 1,
        "modified": 2,
        "removed": 3,
    }

    file_diffs = sorted(file_diffs, key=lambda x: priorities.get(x.status, 4))

    pr_diffs = []
    for file in file_diffs:
        diff = file.patch
        if file.status == "added" or file.status == "modified" or file.status == "removed" or file.status == "renamed":
            pr_diffs.append((file.filename, diff))
        else:
            logger.info(f"File status {file.status} not recognized")  # TODO(sweep): We don't handle renamed files
    return "\n".join([f"{filename}\n{diff}" for filename, diff in pr_diffs])


def parse_issues_from_code_review(issue_string: str):
    issue_regex = r"<issue>(?P<issue>.*?)<\/issue>"
    issue_matches = list(re.finditer(issue_regex, issue_string, re.DOTALL))
    potential_issues = set()
    for issue in issue_matches:
        issue_content = issue.group("issue")
        issue_params = ["issue_description", "file_name", "line_number"]
        issue_args = {}
        issue_failed = False
        for param in issue_params:
            regex = rf"<{param}>(?P<{param}>.*?)<\/{param}>"
            result = re.search(regex, issue_content, re.DOTALL)
            try:
                issue_args[param] = result.group(param).strip()
            except AttributeError:
                issue_failed = True
                break
        if not issue_failed:
            potential_issues.add(CodeReviewIssue(**issue_args))
    return list(potential_issues)


# converts the list of issues inside a code_review into markdown text to display in a github comment
def render_code_review_issues(
    username: str,
    pr: PullRequest,
    code_review: CodeReview,
    issue_type: str = "",
    sorted_issues: list[CodeReviewIssue] = [],  # changes how issues are rendered
):
    files_to_blobs = {file.filename: file.blob_url for file in list(pr.get_files())}
    # generate the diff urls
    files_to_diffs = {}
    for file_name, _ in files_to_blobs.items():
        sha_256 = hashlib.sha256(file_name.encode("utf-8")).hexdigest()
        files_to_diffs[file_name] = f"{pr.html_url}/files#diff-{sha_256}"
    if sorted_issues:
        code_issues = code_review.issues
    else:
        code_issues = code_review.issues
    if issue_type == "potential":
        code_issues = code_review.potential_issues
    code_issues_string = ""
    for issue in code_issues:
        if issue.file_name in files_to_blobs:
            issue_blob_url = f"{files_to_blobs[issue.file_name]}#L{issue.line_number}"
            issue_diff_url = f"{files_to_diffs[issue.file_name]}R{issue.line_number}"
            if sorted_issues:
                code_issues_string += f"<li>In `{issue.file_name}`: {issue.issue_description}</li>\n\n{issue_blob_url}\n[View Diff]({issue_diff_url})"
            else:
                code_issues_string += (
                    f"<li>{issue.issue_description}</li>\n\n{issue_blob_url}\n[View Diff]({issue_diff_url})"
                )
    return code_issues_string


def escape_html(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;")


# make sure code blocks are render properly in github comments markdown
def format_code_sections(text: str) -> str:
    backtick_count = text.count("`")
    if backtick_count % 2 != 0:
        # If there's an odd number of backticks, return the original text
        return text
    result = []
    last_index = 0
    inside_code = False
    while True:
        try:
            index = text.index("`", last_index)
            result.append(text[last_index:index])
            if inside_code:
                result.append("</code>")
            else:
                result.append("<code>")
            inside_code = not inside_code
            last_index = index + 1
        except ValueError:
            # No more backticks found
            break
    result.append(text[last_index:])
    formatted_text = "".join(result)
    # Escape HTML characters within <code> tags
    formatted_text = formatted_text.replace("<code>", "<code>").replace("</code>", "</code>")
    parts = formatted_text.split("<code>")
    for i in range(1, len(parts)):
        code_content, rest = parts[i].split("</code>", 1)
        parts[i] = escape_html(code_content) + "</code>" + rest

    return "<code>".join(parts)


def create_review_comments_for_code_issues(pr: PullRequest, code_issues: list[CodeReviewIssue]):
    commit_sha = pr.head.sha
    commits = list(pr.get_commits())
    pr_commit = None
    for commit in commits:
        if commit.sha == commit_sha:
            pr_commit = commit
            break
    for issue in code_issues:
        comment_body = issue.issue_description
        comment_line = int(issue.line_number)
        comment_path = os.path.normpath(issue.file_name)
        pr.create_review_comment(body=comment_body, commit=pr_commit, path=comment_path, line=comment_line)


# turns code_review_by_file into markdown string
def render_pr_review_by_file(
    username: str,
    pr: PullRequest,
    code_review_by_file: dict[str, CodeReview],
    formatted_comment_threads: dict[str, str],
    pull_request_summary: str = "",
    dropped_files: list[str] = [],
    unsuitable_files: list[tuple[str, Exception]] = [],
    pr_authors: str = "",
) -> str:
    body = f"{SWEEP_PR_REVIEW_HEADER}\n"
    pr_summary = ""
    if pr_authors:
        body += f"Authors: {pr_authors}\n" if ", " in pr_authors else f"Author: {pr_authors}\n"
    # pull request summary goes to the bottom
    if pull_request_summary:
        pr_summary += f"\n<h3>Summary</h3>\n{pull_request_summary}\n<hr>\n"
    issues_section = ""
    code_issues_section = ""
    potential_issues_section = ""
    # build issues section
    # create review comments for all the issues
    all_issues = []
    all_potential_issues = []
    for _, code_review in code_review_by_file.items():
        all_issues.extend(code_review.issues)
        all_potential_issues.extend(code_review.potential_issues)
    create_review_comments_for_code_issues(pr, all_issues)
    # build issues section
    for file_name, code_review in code_review_by_file.items():
        code_issues = code_review.issues
        if code_issues:
            code_issues_string = render_code_review_issues(username, pr, code_review)
            code_issues_section += f"""<details>
<summary>{file_name}</summary>
<ul>{format_code_sections(code_issues_string)}</ul></details>"""
    # build potential issues section
    for file_name, code_review in code_review_by_file.items():
        potential_issues = code_review.potential_issues
        if potential_issues:
            potential_issues_string = render_code_review_issues(username, pr, code_review, issue_type="potential")
            potential_issues_section += f"""<details>
<summary>{file_name}</summary>
<ul>{format_code_sections(potential_issues_string)}</ul></details>"""
    # add titles/dropdowns for issues and potential issues section depending on if there were any issues/potential issues
    if code_issues_section:
        code_issues_section = (
            f"<details><summary><h3>Issues</h3></summary><p><strong>Sweep found these issues in your code.</strong></p>\n\n{code_issues_section}</details><hr>"
            ""
        )
    if potential_issues_section:
        potential_issues_section = f"<details><summary><h3>Potential Issues</h3></summary><p><strong>Sweep is unsure if these are issues, but they might be worth checking out.</strong></p>\n\n{potential_issues_section}</details><hr>"
    # add footer describing dropped files
    footer = ""
    if len(dropped_files) == 1:
        footer += f"<p>{dropped_files[0]} was not reviewed because our filter identified it as typically a non-human-readable (auto-generated) or less important file (e.g., dist files, package.json, images). If this is an error, please let us know.</p>"
    elif len(dropped_files) > 1:
        dropped_files_string = "".join([f"<li>{file}</li>" for file in dropped_files])
        footer += f"<p>The following files were not reviewed because our filter identified them as typically non-human-readable (auto-generated) or less important files (e.g., dist files, package.json, images). If this is an error, please let us know.</p><ul>{dropped_files_string}</ul>"
    if len(unsuitable_files) == 1:
        footer += f"<p>The following file {unsuitable_files[0][0]} were not reviewed as they were deemed unsuitable for the following reason: {str(unsuitable_files[0][1])}. If this is an error please let us know.</p>"
    elif len(unsuitable_files) > 1:
        unsuitable_files_string = "".join(
            [f"<li>{file}: {str(exception)}</li>" for file, exception in unsuitable_files]
        )
        footer += f"<p>The following files were not reviewed as they were deemed unsuitable for a variety of reasons. If this is an error please let us know.</p><ul>{unsuitable_files_string}</ul>"
    if len(all_issues) == 0 and len(all_potential_issues) == 0:
        issues_section = "The Pull Request looks good! Sweep did not find any issues."
        if not formatted_comment_threads:
            issues_section = "The Pull Request looks good! Sweep did not find any new issues."
    elif len(all_issues) == 0:
        issues_section = "The Pull Request looks good! Sweep did not find any issues but found some potential issues that you may want to take a look at."
        if not formatted_comment_threads:
            issues_section = "The Pull Request looks good! Sweep did not find any new issues but found some potential issues that you may want to take a look at."
    else:
        if len(all_issues) == 1:
            issues_section = f"\n\nSweep found `{len(all_issues)}` new issue.\n\n"
        else:
            issues_section = f"\n\nSweep found `{len(all_issues)}` new issues.\n\n"
        issues_section += "Sweep has left comments on the pull request for you to review. \nYou may respond to any comment Sweep made your feedback will be taken into consideration if you run the review again. If Sweep made a mistake, you can resolve the comment or let Sweep know by responding to the comment."
    return body + issues_section + code_issues_section + potential_issues_section + pr_summary + footer


# handles the creation or update of the Sweep comment letting the user know that Sweep is reviewing a pr
# returns the comment_id
def create_update_review_pr_comment(
    username: str,
    pr: PullRequest,
    formatted_comment_threads: dict[str, str],
    code_review_by_file: dict[str, CodeReview] | None = None,
    pull_request_summary: str = "",
    dropped_files: list[str] = [],
    unsuitable_files: list[tuple[str, Exception]] = [],
    error_message: str = "",  # passing in an error message takes priority over everything else
) -> int:
    comment_id = -1
    sweep_comment = None
    # comments that appear in the github ui in the conversation tab are considered issue comments
    pr_comments = list(pr.get_issue_comments())
    # make sure we don't already have a comment created
    for comment in pr_comments:
        # a comment has already been created
        if comment.body.startswith(SWEEP_PR_REVIEW_HEADER):
            comment_id = comment.id
            sweep_comment = comment
            break
    commits = list(pr.get_commits())
    pr_authors = set()
    try:
        pr_authors.add(f"{pr.user.login}")
    except Exception as e:
        logger.error(f"Failed to retrieve {pr.user}: {str(e)}")
    for commit in commits:
        author = commit.author
        try:
            if author:
                pr_authors.add(f"{author.login}")
        except IncompletableObject as e:
            logger.error(f"Failed to retrieve author {author} for commit {commit.sha}: {str(e)}")
    pr_authors = ", ".join(pr_authors)

    # comment has not yet been created
    if not sweep_comment:
        comment_content = f"{SWEEP_PR_REVIEW_HEADER}\nSweep is currently reviewing your pr..."
        if pr_authors:
            comment_content = f"{SWEEP_PR_REVIEW_HEADER}\nAuthors of pull request: {pr_authors}\n\nSweep is currently reviewing your pr..."
        sweep_comment = pr.create_issue_comment(comment_content)

    # update the comment
    if error_message:
        sweep_comment.edit(
            f"{SWEEP_PR_REVIEW_HEADER}\nSweep was unable to review your pull request due to the following reasons:\n\n{error_message}"
        )
        comment_id = sweep_comment.id
        return comment_id  # early return

    # update body of sweep_comment
    if code_review_by_file:
        rendered_pr_review = render_pr_review_by_file(
            username,
            pr,
            code_review_by_file,
            formatted_comment_threads,
            pull_request_summary=pull_request_summary,
            dropped_files=dropped_files,
            unsuitable_files=unsuitable_files,
            pr_authors=pr_authors,
        )
        sweep_comment.edit(rendered_pr_review)
    comment_id = sweep_comment.id
    return comment_id


def format_tracking_id(tracking_id: str | None) -> str:
    if tracking_id:
        return f'\n\n<div align="right"><sup><sup><em>Tracking ID: {tracking_id}</em></sup></sup></div>'
    return ""


def generate_validation_skip_warning() -> str:
    return "> [!WARNING]\n> The issue validation was skipped due to the presence of the `OVERRIDE_ISSUE_VALIDATION` flag. Please ensure that your issue description is clear and actionable."


def generate_revert_pr_comment(commit_message: str, commit_sha: str, pull_request_url: str) -> str:
    formatted_commit_url = f"[{commit_message}]({pull_request_url}/commits/{commit_sha})"
    return (
        f"\n\n# 🔄 Revert {commit_sha}?\nTo revert `{commit_message}` click the checkbox below.\n"
        + f"{PR_REVERT_BUTTON} {formatted_commit_url}"
    )


def get_suffix_for_sweep_comment(tracking_id: str | None, message_marker: str = MESSAGE_MARKER) -> str:
    return DOCUMENTATION_STRING + message_marker + format_tracking_id(tracking_id)

def create_message_marker(marker_id: str) -> str:
    return f"\n\n<!--- MESSAGE_MARKER {marker_id} -->"

def find_sweeps_github_comment(
    issue_or_pr: Issue | PullRequest, message_marker: str = MESSAGE_MARKER
) -> IssueComment | None:
    # NOTE: for pull requests, get_comments only gets review comments, so we need to get issue comments too if it's a pull request
    all_comments = chain(
        issue_or_pr.get_comments(),
        (issue_or_pr.get_issue_comments() if isinstance(issue_or_pr, PullRequest) else []),
    )
    return next((comment for comment in all_comments if message_marker in comment.body), None)


def create_or_edit_sweeps_github_comment(
    issue_or_pr: Issue | PullRequest,
    sweeps_message: str,
    sweeps_github_comment: IssueComment | None = None,
    tracking_id: str | None = None,
    message_marker: str = MESSAGE_MARKER,
) -> IssueComment:
    """
    If this is not used to exit, return the sweeps_github_comment so that the caller can edit it.
    """
    # existing comment exists, edit the comment
    body = sweeps_message + get_suffix_for_sweep_comment(tracking_id, message_marker)
    if sweeps_github_comment:
        sweeps_github_comment.edit(body=body)
    else:
        sweeps_github_comment = find_sweeps_github_comment(issue_or_pr, message_marker)
        if sweeps_github_comment:
            sweeps_github_comment.edit(body=body)
        else:
            # no existing comment exists, create the comment
            if isinstance(issue_or_pr, PullRequest):
                sweeps_github_comment = issue_or_pr.create_issue_comment(body)
            elif isinstance(issue_or_pr, Issue):
                sweeps_github_comment = issue_or_pr.create_comment(body)
    return sweeps_github_comment


@dataclass
class UserFacingError(Exception):
    message: str


TRACEBACK_FORMAT = """## ❌ {error_title}

```
{traceback}
```

<b>{message}</b>"""


@contextmanager
def user_facing_error(message: str | Callable[[Exception], str]):
    try:
        yield
    except Exception as e:
        if callable(message):
            raise UserFacingError(message(e)) from e
        else:
            raise UserFacingError(message) from e


@dataclass
class IssueErrorHandler:
    issue: Issue
    error_title: str = "Error"
    comment: IssueComment | PullRequestComment | None = None
    tracking_id: str | None = None
    do_delete: bool = False

    def format_error(self, e: Exception, tb: str):
        mailto_link = f'<a href="mailto:support@sweep.dev?subject=Sweep%20Error:%20tracking%20id%20{self.tracking_id}&body=Sending this email to let you know that Sweep encountered an error. Thank you.">via this link</a>'
        error_message = TRACEBACK_FORMAT.format(error_title=self.error_title, traceback=tb, message=str(e))
        support_message = f"\n\nSweep has encountered a runtime error unrelated to your request. Please let us know {mailto_link} or at support@sweep.dev directly."
        result = error_message + support_message
        return sanitize_string_for_github(result)

    def display_error(self, e: Exception):
        tb = traceback.format_exc()
        if self.comment:
            self.comment.edit(
                body=self.format_error(e, tb)
                + MESSAGE_MARKER
                + DOCUMENTATION_STRING
                + format_tracking_id(self.tracking_id)
            )
        else:
            create_or_edit_sweeps_github_comment(
                issue_or_pr=self.issue,
                sweeps_message=self.format_error(e, tb),
                sweeps_github_comment=None,
                tracking_id=self.tracking_id,
            )

    def delete_comment(self):
        if self.comment:
            self.comment.delete()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            if exc_type not in (KeyboardInterrupt, SystemExit, BdbQuit):  # noqa: E721
                self.display_error(exc_value)
            return False
        elif self.do_delete:
            self.delete_comment()
        return True
