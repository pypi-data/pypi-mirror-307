import os
import re

from github.IssueComment import IssueComment
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from github.Repository import Repository
from loguru import logger

from sweepai.backend.api import fix_issue
from sweepai.backend.api_utils import get_pr_snippets
from sweepai.ci.cleanup_ci import clean_ci_logs
from sweepai.core.entities import UserMessage
from sweepai.core.github_utils import ClonedRepo, get_github_client
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.dataclasses.fix_issue_result import FixIssueResult
from sweepai.ci.fetch_ci import create_hyperlink, get_ci_failure_logs, get_ci_failures
from sweepai.handlers.format_issue_results import format_results
from sweepai.o11y.log_utils import log_to_file, log_warnings_to_file
from sweepai.o11y.posthog_trace import posthog_trace
from sweepai.utils.diff import remove_whitespace_changes
from sweepai.utils.str_utils import code_block, format_comment_prompt_from_files, markdown_list, strip_sweep, blockquote, tail, wrap_xml_tag
from sweepai.utils.ticket_rendering_utils import (
    HR,
    IssueErrorHandler,
    center,
    create_message_marker,
    create_or_edit_sweeps_github_comment,
    generate_revert_pr_comment,
    get_suffix_for_sweep_comment,
    sweeping_png,
)
from sweepai.web.validate_license import validate_license

num_of_snippets_to_query = 30
total_number_of_snippet_tokens = 15_000
num_full_files = 2
num_extended_snippets = 2

ERROR_FORMAT = "❌ {title}\n\nPlease report this on our [community forum](https://community.sweep.dev/)."
SWEEPING_GIF = f"{center(sweeping_png)}\n\n"


def get_original_issue(pull_request: PullRequest):
    pattern = r"Fixes\s+#(?P<issue_number>\d+)"
    if match := re.search(pattern, pull_request.body):
        repo = pull_request.base.repo
        issue_number = match.group("issue_number")
        issue = repo.get_issue(int(issue_number))
        return issue
    return None


def get_actor_from_pull_request(pull_request: PullRequest):
    author = pull_request.user
    if author.type != "Bot":
        return author.login

    for assignee in pull_request.assignees:
        if assignee.type != "Bot":
            return assignee.login
    original_issue = get_original_issue(pull_request)

    if original_issue and original_issue.user.type != "Bot":
        return original_issue.user.login

    return author.login

def summarize_ci_logs(logs_list: list, pull_request: PullRequest, username: str) -> str:
    repo_full_name = pull_request.base.repo.full_name
    
    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_full_name, branch=pull_request.head.ref)
    pull_request_metadata = generate_pull_request_metadata(pull_request)
    _, _, pulls_message = get_pr_snippets(
        repo_name=repo_full_name,
        annotations={"pulls": pull_request_metadata},
        cloned_repo=cloned_repo,
        context=ChatAgentContext(use_case="ticket"),
    )
    cleaned_logs = clean_ci_logs(
        username=username,
        error_logs=logs_list[0],
        pulls_message=pulls_message,
    )
    return cleaned_logs

def get_ci_data(
    pull_request: PullRequest,
    username: str,
    installation_id: int,
):
    # Fetching CI data
    _pending_runs, _successful_runs, error_runs = get_ci_failures(pull_request)
    logs_list = get_ci_failure_logs(installation_id, error_runs, pull_request)

    # Cleaning CI logs
    if logs_list:
        joined_logs = markdown_list([create_hyperlink(run) for run in error_runs])
        cleaned_logs = summarize_ci_logs(logs_list, pull_request, username)
        ci_comment_body = f" I'm working on this. I also see the following CI errors:\n\n{code_block(tail(cleaned_logs, max_lines=20))}\n\nSources:\n\n{joined_logs}"
    else:
        cleaned_logs = ""
        ci_comment_body = ""
    
    return cleaned_logs, ci_comment_body


def generate_pull_request_metadata(pull_request: PullRequest):
    file_diffs = [
        {
            "sha": pull_request_file.sha,
            "filename": pull_request_file.filename,
            "status": pull_request_file.status,
            "additions": pull_request_file.additions,
            "deletions": pull_request_file.deletions,
            "changes": pull_request_file.changes,
            "blob_url": pull_request_file.blob_url,
            "raw_url": pull_request_file.raw_url,
            "contents_url": pull_request_file.contents_url,
            "patch": remove_whitespace_changes(
                pull_request_file.patch or ""
            ),  # for one java formatting change, we went from 100k chars to 67k chars
            "previous_filename": pull_request_file.previous_filename,
        }
        for pull_request_file in pull_request.get_files()
    ]
    pull_request_metadata = [
        {
            "number": pull_request.number,
            "repo_name": pull_request.base.repo.name,
            "title": pull_request.title,
            "body": pull_request.body,
            "labels": pull_request.labels,
            "status": pull_request.state,
            "file_diffs": file_diffs,
            "branch": pull_request.head.ref,
        }
    ]
    return pull_request_metadata


def generate_revert_comment_and_format_results(
    repo: Repository,
    fix_issue_result: FixIssueResult,
    fix_string: str,
    tracking_id: str,
):
    assert (
        new_pull_request_number := fix_issue_result.pull_request_data.number
    ) is not None, "New pull request number is None"
    new_pull_request = repo.get_pull(new_pull_request_number)
    commit_sha = new_pull_request.head.sha
    revert_pr_comment = generate_revert_pr_comment(
        commit_message=new_pull_request.title,
        commit_sha=commit_sha,
        pull_request_url=new_pull_request.html_url,
    )
    response = format_results(fix_issue_result, fix_string, repo, tracking_id, is_comment=True)
    return response + revert_pr_comment


@posthog_trace
async def on_comment(
    username: str,
    repo_full_name: str,
    installation_id: int,
    pr_number: int,
    comment_id: int,
    tracking_id: str | None = None,
):
    if not os.environ.get("CLI"):
        assert (
            validate_license()
        ), "License key is invalid or expired. Please contact us at team@sweep.dev to upgrade to an enterprise license."

    with log_to_file(tracking_id), log_warnings_to_file(keywords=["[YELLOW]"], tracking_id=tracking_id):
        access_token, g = get_github_client(installation_id)
        repo: Repository = g.get_repo(repo_full_name)
        pull_request: PullRequest = repo.get_pull(pr_number)
        logger.info(f"URL: {pull_request.html_url}")

        # Try to get the comment as a PullRequestComment first
        sweeps_github_comment = None
        with IssueErrorHandler(
            pull_request.as_issue(),
            error_title="Error while processing comment",
            tracking_id=tracking_id,
        ) as monitor:
            original_user_comment = try_get_issue_or_review_comment(comment_id, pull_request)
            logger.info(f"Original user comment: {original_user_comment.html_url}")

            stripped_comment_body = strip_sweep(original_user_comment.body)
            # Create a reply comment depending on the type of comment
            comment_body = f"{blockquote(stripped_comment_body)}\n\nThanks for the comment, @{username}! I'm working on this. This should take about 5-10 min."
            if isinstance(original_user_comment, PullRequestComment):
                sweeps_github_comment = pull_request.create_review_comment_reply(
                    comment_id,
                    comment_body + get_suffix_for_sweep_comment(tracking_id=tracking_id),
                )
            else:
                sweeps_github_comment = create_or_edit_sweeps_github_comment(
                    issue_or_pr=pull_request,
                    sweeps_message=comment_body,
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                    message_marker=create_message_marker(original_user_comment.html_url),
                )

            monitor.comment = sweeps_github_comment

            # Fetching CI data
            cleaned_logs, ci_comment_body = get_ci_data(pull_request, username, installation_id)

            if ci_comment_body:
                comment_body = f"{blockquote(stripped_comment_body)}\n\nThanks for the comment, @{username}!" + ci_comment_body + "\n\nThis should take about 5-10 min."

                create_or_edit_sweeps_github_comment(
                    issue_or_pr=pull_request,
                    sweeps_message=comment_body,
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )

            ### Running Sweep

            pull_request_head_branch = pull_request.head.ref
            pull_request_url = pull_request.html_url
            query = f"Address the following pull request comment"
            # Case 1: Comment is a review comment we can print comment inline with the diff
            if (
                hasattr(original_user_comment, "path")
                and hasattr(original_user_comment, "position")
                and hasattr(original_user_comment, "diff_hunk")
            ):
                query += format_comment_prompt_from_files(
                    comment_path=original_user_comment.path,
                    comment_position=original_user_comment.position,
                    comment_diff_hunk=original_user_comment.diff_hunk,
                    comment_body=stripped_comment_body,
                )
            # Case 2: Comment is an issue comment we can print the comment as a normal comment
            elif hasattr(original_user_comment, "path"):
                query += f" in the file {original_user_comment.path}:\n{stripped_comment_body}"
            # Case 3: Something went wrong, we can print the comment as a normal comment
            else:
                query += f":\n{stripped_comment_body}"

            if cleaned_logs: # TODO: make this routable, don't always include it
                query += f"\n\nAlso, here are the failing CI logs:\n\n" + wrap_xml_tag(cleaned_logs, "failing_ci_logs")

            # This instantiates all of the pull request context for Sweep, simply passing in the URL is not sufficient
            pull_request_metadata = generate_pull_request_metadata(pull_request)
            # Now we run Sweep
            fix_string = f"# Fixes\n > [{stripped_comment_body}]({original_user_comment.html_url})\n\nIn pull request {pull_request_url}\n\n"
            try:
                fix_issue_result = await fix_issue(
                    repo_full_name=repo_full_name,
                    query=query,
                    access_token=access_token,
                    messages=[UserMessage(content=query)],
                    snippets=[],
                    branch=pull_request_head_branch,
                    username=username,
                    pulls=pull_request_metadata,
                )
                comment_body = f"{blockquote(stripped_comment_body)}\n\nHey, @{username}, I finished working on this. Here are the changes I made:"
                response = comment_body + HR + format_results(fix_issue_result, fix_string, repo, tracking_id, is_comment=True)
                create_or_edit_sweeps_github_comment(
                    issue_or_pr=pull_request,
                    sweeps_message=response,
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )
                # TODO: update comment body to be simpler
                response = comment_body + HR + generate_revert_comment_and_format_results(repo, fix_issue_result, fix_string, tracking_id)
                create_or_edit_sweeps_github_comment(
                    issue_or_pr=pull_request,
                    sweeps_message=response,
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )
                return fix_issue_result
            except Exception as e:
                create_or_edit_sweeps_github_comment(
                    issue_or_pr=pull_request,
                    sweeps_message=f"Error: {str(e)}",
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )
                raise e


def try_get_issue_or_review_comment(comment_id: int, pull_request: PullRequest) -> PullRequestComment | IssueComment:
    try:
        comment: PullRequestComment = pull_request.get_review_comment(comment_id)
    except Exception:
        # If it fails, try to get it as an IssueComment
        try:
            comment: IssueComment = pull_request.get_issue_comment(comment_id)
        except Exception as e:
            # Both attempts failed, notify the user
            error_message = f"Failed to retrieve the comment. Error: {str(e)}"
            pull_request.create_issue_comment(error_message)
            raise ValueError(f"Unable to retrieve comment: {error_message}")
    return comment
