"""
on_ticket is the main function that is called when a new issue is created.
It is only called by the webhook handler in sweepai/api.py.
"""

import os
import re

from github.Issue import Issue
from github.IssueComment import IssueComment
from loguru import logger

from sweepai.backend.api import fix_issue
from sweepai.backend.request_rewriter import rewrite_query
from sweepai.config.server import FRONTEND_URL, SWEEP_ISSUE_ALLOWLIST
from sweepai.core.entities import UserMessage
from sweepai.core.github_utils import ClonedRepo, get_github_client, has_repo_been_cloned_before
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.handlers import handlers_cache
from sweepai.handlers.fix_ci import fix_ci_failures
from sweepai.handlers.format_issue_results import format_results
from sweepai.handlers.issue_validator import validate_issue
from sweepai.o11y.log_utils import log_to_file, log_warnings_to_file
from sweepai.o11y.posthog_trace import posthog_trace
from sweepai.utils.str_utils import strip_sweep, wildcard_match
from sweepai.utils.ticket_rendering_utils import (
    OVERRIDE_ISSUE_VALIDATION,
    IssueErrorHandler,
    UserFacingError,
    center,
    create_or_edit_sweeps_github_comment,
    generate_validation_skip_warning,
    sweeping_png,
    user_facing_error,
)
from sweepai.web.validate_license import validate_license


def extract_branch_from_description(summary: str) -> tuple[str, str]:
    branch_match = re.search(r"^branch:\s*(\S+)", summary, re.MULTILINE)
    branch = branch_match.group(1) if branch_match else None
    summary = re.sub(r"^branch:\s*\S+\s*\n?", "", summary, flags=re.MULTILINE).strip()
    return branch, summary


def is_sweep_issue_enabled_for_user(username: str) -> bool:
    return wildcard_match(username, SWEEP_ISSUE_ALLOWLIST)


def validate_issue_and_create_comment(
    issue: Issue,
    tracking_id: str,
    title: str,
    summary: str,
    sweeps_github_comment: IssueComment | None = None,
) -> tuple[bool, IssueComment | None, bool]:
    override_validation = OVERRIDE_ISSUE_VALIDATION in summary
    is_issue_valid = True
    validation_skipped = False
    if not override_validation:
        is_issue_valid, validator_response = validate_issue(title + "\n\n" + summary)
        if not is_issue_valid:
            sweeps_github_comment = create_or_edit_sweeps_github_comment(
                issue_or_pr=issue,
                sweeps_message=validator_response,
                sweeps_github_comment=sweeps_github_comment,
                tracking_id=tracking_id,
            )
    else:
        validation_skipped = True

    return is_issue_valid, sweeps_github_comment, validation_skipped


@posthog_trace
async def on_ticket(
    username: str,
    title: str,
    summary: str | None,
    issue_number: int,
    repo_full_name: str,
    installation_id: int,
    is_first_sweep_invocation: bool = True,  # Whether this is the first time Sweep is being invoked for this issue
    tracking_id: str | None = None,
):
    if not os.environ.get("CLI") and not validate_license():
        raise UserFacingError(
            "License key is invalid or expired. Please contact us at team@sweep.dev to upgrade to an enterprise license."
        )
    with log_to_file(tracking_id), log_warnings_to_file(
        keywords=["[YELLOW]"], tracking_id=tracking_id
    ):  # this will catch all LLM calls from modify
        access_token, g = get_github_client(installation_id)
        repo = g.get_repo(repo_full_name)
        issue = repo.get_issue(number=issue_number)
        logger.info(f"URL: {issue.html_url}")

        with IssueErrorHandler(issue, tracking_id=tracking_id) as monitor:
            title = strip_sweep(title)
            summary = summary or ""
            branch, summary = extract_branch_from_description(summary=summary)
            sweeps_github_comment = None

            # validate that the branch exists
            with user_facing_error(f"Branch {branch} does not exist. Please create/restore the branch and try again."):
                branch = branch if branch else repo.default_branch
                if branch != repo.default_branch and not repo.get_branch(branch):
                    raise Exception(f"Branch {branch} does not exist. Please create/restore the branch and try again.")

            if not is_sweep_issue_enabled_for_user(username):  # disabled in prod, enabled for some enterprise users
                create_or_edit_sweeps_github_comment(
                    issue_or_pr=issue,
                    sweeps_message="❌ The ticket to PR workflow is no longer supported. We have moved to a new chat interface in private beta. Please contact us at team@sweep.dev to try it out.",
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )
                return

            acknowledgement_message = f"{center(sweeping_png)}\n\nThanks for the ticket, @{username}!\nI'm currently adding more details to your issue description. This should take about 1 minute."  # Indicate if first time indexing
            sweeps_github_comment = create_or_edit_sweeps_github_comment(
                issue_or_pr=issue,
                sweeps_message=acknowledgement_message,
                sweeps_github_comment=sweeps_github_comment,
                tracking_id=tracking_id,
            )
            monitor.comment = sweeps_github_comment
            # on the first invocation, we want to rewrite the issue body
            # on subsequent invocations, we want to continue the conversation
            if is_first_sweep_invocation:
                if not has_repo_been_cloned_before(
                    repo_full_name=repo.full_name,
                    branch=branch if branch != repo.default_branch else None,
                ):
                    cloning_message = (
                        f"{center(sweeping_png)}\n\nCloning repository {repo.full_name}... This might take a while!"
                    )
                    sweeps_github_comment = create_or_edit_sweeps_github_comment(
                        issue_or_pr=issue,
                        sweeps_message=cloning_message,
                        sweeps_github_comment=sweeps_github_comment,
                        tracking_id=tracking_id,
                    )
                cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_full_name, branch=branch)
                pulls = []  # for now this should never be populated
                # REWRITE - we add more details to the issue body here
                _, new_ticket, _ = rewrite_query(
                    username=username,
                    question=f"{title}\n\n{summary}",
                    cloned_repo=cloned_repo,
                    pulls=pulls,
                    model=LATEST_CLAUDE_MODEL,
                    context=ChatAgentContext(use_case="ticket"),
                ) # type: ignore
                # VALIDATE - we validate the issue body here
                is_issue_valid, sweeps_github_comment, validation_skipped = validate_issue_and_create_comment(
                    issue=issue,
                    tracking_id=tracking_id,
                    title=title,
                    summary=f"{summary}\n\n---\n\n{new_ticket}",
                    sweeps_github_comment=sweeps_github_comment,
                )
                if not is_issue_valid:
                    return
                # UPDATE USER - we update the issue body here only if the issue is valid
                acknowledgement_message = f"{center(sweeping_png)}\n\nThanks for the ticket, @{username}!\nI've added more details to your issue description (see above).\n\n:pushpin: From now on, I will use your issue description as-is and won't make further edits. If you'd like to add more details, please use our frontend at {FRONTEND_URL}."
                issue.edit(body=f"{summary}\n\n---\n\n{new_ticket}")
                sweeps_github_comment = create_or_edit_sweeps_github_comment(
                    issue_or_pr=issue,
                    sweeps_message=acknowledgement_message,
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )
            else:
                is_issue_valid, sweeps_github_comment, validation_skipped = validate_issue_and_create_comment(
                    issue=issue,
                    tracking_id=tracking_id,
                    title=title,
                    summary=summary,
                    sweeps_github_comment=sweeps_github_comment,
                )
                if not is_issue_valid:
                    return
                acknowledgement_message = f"{center(sweeping_png)}\n\nThanks for the ticket, @{username}!\nI'm working on this. This should take about 5-10 min."
                sweeps_github_comment = create_or_edit_sweeps_github_comment(
                    issue_or_pr=issue,
                    sweeps_message=acknowledgement_message,
                    sweeps_github_comment=sweeps_github_comment,
                    tracking_id=tracking_id,
                )
                new_ticket = ""

            # Remove OVERRIDE_ISSUE_VALIDATION from the summary before fixing issue
            summary = summary.replace(OVERRIDE_ISSUE_VALIDATION, "").strip()

            # this ternary is to ensure that the title is not duplicated (Sweep doesn't actually make edits to title)
            query = (
                f"# {title}\n\n{summary}\n\n---\n\n{new_ticket}"
                if title not in new_ticket
                else f"{summary}\n\n---\n\n{new_ticket}"
            )

            # this actually runs the issue. in the future we will add CI/CD within this section
            fix_issue_result = await fix_issue(
                repo_full_name=repo.full_name,
                query=query,
                access_token=access_token,
                messages=[UserMessage(content=query)],
                snippets=[],
                branch=branch,
                username=username,
            )
            handlers_cache.set(issue.html_url, fix_issue_result)
            response = format_results(
                fix_issue_result,
                f"# Fixes\nFixes #{issue_number}",  # links the dev branch
                repo,
                tracking_id,
            )
            sweeps_github_comment = create_or_edit_sweeps_github_comment(
                issue_or_pr=issue,
                sweeps_message=response,
                sweeps_github_comment=sweeps_github_comment,
                tracking_id=tracking_id,
            )

            if fix_issue_result.pull_request_data:
                pull_request = repo.get_pull(fix_issue_result.pull_request_data.number)
                handlers_cache.set(fix_issue_result.pull_request_data.html_url, fix_issue_result)
                if validation_skipped:
                    pull_request.edit(
                        body=generate_validation_skip_warning()
                        + "\n\n"
                        + fix_issue_result.pull_request_data.description
                    )
                await fix_ci_failures(pull_request, tracking_id=tracking_id)
