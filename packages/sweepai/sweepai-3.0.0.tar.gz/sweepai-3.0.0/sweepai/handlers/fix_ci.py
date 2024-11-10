from github.Commit import Commit
from github.GithubException import GithubException
from github.PullRequest import PullRequest
from loguru import logger
from tqdm import tqdm

from sweepai.backend.api import fix_issue
from sweepai.backend.api_utils import get_pr_snippets
from sweepai.config.server import (
    FIX_CI_ALLOWLIST,
    GITHUB_BASE_URL,
)
from sweepai.core.entities import Snippet, snippet_to_string, organize_snippets
from sweepai.core.github_utils import ClonedRepo, get_github_repo, get_installation_id
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.dataclasses.fix_issue_result import FixIssueResult
from sweepai.handlers import handlers_cache
from sweepai.handlers.format_issue_results import (
    extract_diff_patches,
    format_results,
    format_results_body,
)
from sweepai.handlers.on_comment import (
    generate_pull_request_metadata,
    generate_revert_comment_and_format_results,
    get_actor_from_pull_request,
)
from sweepai.ci.cleanup_ci import clean_ci_logs
from sweepai.ci.summarize_history import summarize_history
from sweepai.modify.modify_utils import english_join
from sweepai.o11y.log_utils import log_to_file
from sweepai.search.agent.agent_utils import get_all_snippets_from_query
from sweepai.utils.format_utils import Prompt
from sweepai.utils.str_utils import (
    code_block,
    markdown_list,
    pack_items_for_prompt,
    tail,
    truncate_text_width,
    wildcard_match,
)
from sweepai.utils.ticket_rendering_utils import (
    HR,
    IssueErrorHandler,
    find_sweeps_github_comment,
    get_suffix_for_sweep_comment,
)
from sweepai.ci.fetch_ci import FixCIInput, create_hyperlink, get_ci_failure_logs, interval_timer, wait_for_ci_failures

### CACHE LOGIC

def get_existing_snippets(pull_request: PullRequest, cloned_repo: ClonedRepo) -> list[Snippet]:
    fix_issue_result: FixIssueResult | None = handlers_cache.get(pull_request.html_url, None)
    if not isinstance(fix_issue_result, FixIssueResult):
        return []
    snippets = fix_issue_result.snippets # from on_ticket.py
    if fix_ci_history := get_ci_history(pull_request):
        # TODO: add logic to clear reverted changes
        _, last_result = fix_ci_history[-1]
        if not last_result:
            return []
        snippets = last_result.snippets
    # replace/handle contents and lines here because they might be stale from a previous commit
    cleaned_and_deduped_snippets = []
    for snippet in snippets:
        try:
            snippet.content = cloned_repo.get_file_contents(snippet.file_path)
            snippet.end = min(snippet.end, snippet.content.count("\n"))
            cleaned_and_deduped_snippets.append(snippet)
        except FileNotFoundError:
            logger.info(f"File {snippet.file_path} not found in cloned repo")
            continue
    # deduplicate snippets
    cleaned_and_deduped_snippets = organize_snippets(cleaned_and_deduped_snippets)
    return cleaned_and_deduped_snippets


def get_ci_history(
    pull_request: PullRequest,
) -> list[tuple[FixCIInput, FixIssueResult]]:
    repo = pull_request.base.repo
    handlers_cache_key = f"ci_fix_history-{pull_request.html_url}"
    history = handlers_cache.get(handlers_cache_key, [])
    if history and isinstance(history[0], dict):  # for temporary backwards compatibility
        history = [FixIssueResult(**result) for result in history]
    return [
        (inp, result)
        for inp, result in history
        if "revert" not in repo.get_commit(inp.commit_hash).commit.message.lower()
    ]


def append_to_ci_history(pull_request: PullRequest, history: list[tuple[FixCIInput, FixIssueResult]]):
    handlers_cache_key = f"ci_fix_history-{pull_request.html_url}"
    handlers_cache.set(handlers_cache_key, [*handlers_cache.get(handlers_cache_key, []), *history])


# -%} will make it single line joined
render_history_prompt = Prompt(
    """
{% for inp, result in history -%}
<fix_attempt index="{{ loop.index }}">
{{ inp.cleaned_logs | trim('\n') | wrap_xml("error_logs") }}
{{ format_results_body(result) | trim('\n') | wrap_xml("fixes") }}
</fix_attempt>
{% endfor %}
""",
    globals=[format_results_body],
)


def render_history(pull_request: PullRequest) -> str:
    history = get_ci_history(pull_request)
    # sometimes we write bad PRs to the cache
    history = [(inp, result) for inp, result in history if result.pull_request_data]
    history_str = render_history_prompt.render(history=history)
    return history_str


def get_last_error_log(cleaned_logs: str) -> str:
    lines = cleaned_logs.splitlines()
    MAX_LINE_LENGTH = 300
    backup_line = lines[-1][:MAX_LINE_LENGTH]
    lines = [line for line in lines if len(line) < MAX_LINE_LENGTH]
    if answer := next((line for line in lines[::-1] if "Error" in line), None):
        return answer
    if answer := next((line for line in lines[::-1] if "error" in line.lower()), None):
        return answer
    return backup_line


render_history_for_github_comment_prompt = Prompt(
    """
{% if history and len(history) > 0 %}
I'm currently working on fixing the CI errors. Here were all my previous attempts:

{% if len(history) > 10 %}
...
{% endif %}

{% for (inp, result), commit_message in zip(history, commit_messages) -%}
{% if loop.index > len(history) - 10 %}
<details>
<summary>{{ loop.index }}. <a href="https://{{GITHUB_BASE_URL}}/{{repo.full_name}}/commit/{{inp.commit_hash}}">{{commit_message}} ({{inp.commit_hash[:7]}})</a> to fix the following error:

<pre>
{{ inp.cleaned_logs | tail(max_lines=20) | truncate_text_width(width=200) }}
</pre>
</summary>

#### Attempted Fix

<blockquote>

{{ extract_diff_patches(result) }}
</blockquote>
</details>
{% endif %}
{% endfor %}

---

{% endif %}
""",
    globals=[extract_diff_patches, zip, get_last_error_log, len],
    filters=[tail, english_join, truncate_text_width],
    constants={"GITHUB_BASE_URL": GITHUB_BASE_URL},
)


def get_patch_from_commit(commit: Commit) -> str:
    return "\n\n".join(data["patch"] for data in commit.raw_data["files"])


def render_history_for_github_comment(
    pull_request: PullRequest, history: list[tuple[FixCIInput, FixIssueResult]]
) -> str:
    # TODO: add summary of number of lines changed
    # TODO: add timestamps
    repo = pull_request.base.repo
    commit_data = {}
    children = {}
    pr_commits = list(tqdm(pull_request.get_commits(), desc="Fetching commits"))
    for commit, next_commit in zip(pr_commits, [None] + pr_commits):
        commit_data[commit.sha] = commit
        if next_commit:
            children[next_commit.sha] = commit.sha
    commits = []
    commit_messages = []
    for inp, _result in history:
        # I don't fully trust the code here, very easy to get a key error, so I'm doing this
        if inp.commit_hash not in commit_data:
            logger.warning(f"Commit {inp.commit_hash} not found in commit_data or children")
            continue
        if inp.commit_hash not in children:
            logger.warning(f"Commit {inp.commit_hash} not found in children")
            continue
        if children[inp.commit_hash] not in commit_data:
            logger.warning(f"Commit {children[inp.commit_hash]} not found in commit_data")
            continue
        commits.append(commit_data[inp.commit_hash])
        commit_messages.append(commit_data[children[inp.commit_hash]].commit.message)
    return render_history_for_github_comment_prompt.render(history=history, repo=repo, commit_messages=commit_messages)


### MAIN


async def fix_ci_failures_once(
    pull_request: PullRequest,
    tracking_id: str | None = None,
    force: bool = False,
):
    if pull_request.state != "open" and not force:
        return
    comment = find_sweeps_github_comment(pull_request)
    with log_to_file(tracking_id), IssueErrorHandler(
        pull_request.as_issue(),
        error_title="Error while fixing CI",
        tracking_id=tracking_id,
    ) as monitor:
        logger.info(f"URL: {pull_request.html_url}")
        repo = pull_request.base.repo
        repo_full_name = repo.full_name
        org_name, repo_name = repo_full_name.split("/")
        access_token = repo._requester.auth.token
        installation_id = get_installation_id(username=org_name)
        username = get_actor_from_pull_request(pull_request)
        branch = pull_request.head.ref
        commit: Commit = pull_request.get_commits().reversed[0]
        commit_link = create_hyperlink(commit)
        SWEEP_SETTINGS_PAGE = f"https://{GITHUB_BASE_URL}/organizations/{org_name}/settings/installations/{installation_id}"  # TODO: support user configs

        ci_history = get_ci_history(pull_request)
        markdown_history = render_history_for_github_comment(pull_request, ci_history)
        message = (
            markdown_history
            + f"\n\nI'm currently monitoring {commit_link} for CI failures. This should take about 5-10 min."
            + get_suffix_for_sweep_comment(tracking_id)
        )
        if comment:
            comment.edit(body=message)
        else:
            comment = pull_request.create_issue_comment(message)
        monitor.comment = comment

        # Wait for CI failures
        try:
            pending_runs, successful_runs, error_runs = wait_for_ci_failures(pull_request)
        except GithubException as e:
            if e.status == 403:
                comment.edit(
                    body=f"I couldn't access the CI status. Please make sure to give Sweep access to your GitHub repository at https://{GITHUB_BASE_URL}/organizations/{org_name}/settings/installations/{installation_id}."
                    + get_suffix_for_sweep_comment(tracking_id)
                )
                return
            raise

        # Fetching logs
        if not error_runs:
            logger.info("No error runs found")
            if ci_history:
                # Used to have error runs, no longer do, meaning the CI errors have been fixed
                comment.edit(
                    body=markdown_history.replace(
                        "I'm currently working on fixing the CI errors. Here were all my previous attempts:",
                        "**✨ The CI errors have been fixed! ✨**\n\nHere's what I did:",
                    )
                    + f"\n\nIf you think this is an error, check Sweep's permissions at {SWEEP_SETTINGS_PAGE}."
                    + get_suffix_for_sweep_comment(tracking_id)
                )
            else:
                if pending_runs or successful_runs:
                    # Only pending or successful runs
                    comment.edit(
                        body=markdown_history
                        + f"\n\nNo CI failures were found. If you think this is an error, check Sweep's permissions at {SWEEP_SETTINGS_PAGE}."
                        + get_suffix_for_sweep_comment(tracking_id)
                    )
                else:
                    # No runs at all
                    comment.edit(
                        body=markdown_history
                        + f"\n\nNo CI runs were found. Sweep can fix CI failures, so we recommend setting it up for your repository to let Sweep run your build and tests.\n\nIf you think this is an error, check Sweep's permissions at {SWEEP_SETTINGS_PAGE}."
                        + get_suffix_for_sweep_comment(tracking_id)
                    )
            return
        logs_list = []
        # TODO: make this it's own function
        for i in interval_timer(total_time=60 * 10):
            logs_list = get_ci_failure_logs(installation_id=installation_id, runs=error_runs, pull_request=pull_request)
            if logs_list:
                logger.info(f"Found info logs here:\n {logs_list[-10000:]}")
                break

        if not logs_list:
            comment.edit(
                body=markdown_history
                + f"\n\nSome of the CI runs failed, but I couldn't access the logs. Check Sweep's permissions at {SWEEP_SETTINGS_PAGE}."
                + get_suffix_for_sweep_comment(tracking_id)
            )
            return

        if not wildcard_match(username, FIX_CI_ALLOWLIST):
            comment.edit(
                body=f"Hey @{username}, CI auto-fix is currently not enabled for you. Please reach out to the [Sweep team](william@sweep.dev) to enable it."
                + get_suffix_for_sweep_comment(tracking_id)
            )
            return

        joined_logs = markdown_list([create_hyperlink(run) for run in error_runs])
        initial_message = (
            markdown_history
            + f"\n\nI currently see that the following CI runs are failing for {commit_link}:\n{joined_logs}\n\nHere are some of the logs:\n\n```\n...\n{tail(logs_list[0], max_lines=20)}\n```\n\nI'm currently trying to fix them. This should take about 5-10 min."
        )
        comment.edit(body=initial_message + get_suffix_for_sweep_comment(tracking_id))
        cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_full_name, branch=branch)

        pull_request_metadata = generate_pull_request_metadata(pull_request)
        _, _, pulls_message = get_pr_snippets(
            repo_name=repo_full_name,
            annotations={"pulls": pull_request_metadata},
            cloned_repo=cloned_repo,
            context=ChatAgentContext(use_case="ci"),
        )
        
        # Logs cleanup
        cleaned_logs = clean_ci_logs(
            username=username,
            error_logs=logs_list[0],
            pulls_message=pulls_message,
        )

        # Summarize history of previous CI runs
        summarized_history = summarize_history(username=username, history=render_history(pull_request), current_failing_error_logs=cleaned_logs)

        context = ChatAgentContext(
            use_case="ci",
            history=summarized_history,
        )

        initial_message = (
            markdown_history
            + f"\n\nI currently see that the following CI runs are failing for {commit_link}:\n{joined_logs}\n\nHere are some of the logs:\n\n{code_block(tail(cleaned_logs, max_lines=20))}\n\nI'm currently trying to fix them. This should take about 5-10 min."
        )
        comment.edit(body=initial_message + get_suffix_for_sweep_comment(tracking_id))

        query = cleaned_logs

        pull_request_changed_snippets = get_existing_snippets(pull_request=pull_request, cloned_repo=cloned_repo)
        ci_mentioned_snippets = get_all_snippets_from_query(query=cleaned_logs, cloned_repo=cloned_repo)
        # Put pull_request_changed_snippets second because it's at least in the diff
        ci_snippets: list[Snippet] = organize_snippets(ci_mentioned_snippets + pull_request_changed_snippets)
        # need to make sure mentioned snippets are always there
        ci_snippets: list[Snippet] = pack_items_for_prompt(
            iterable=ci_snippets, string_function=snippet_to_string, token_limit=50_000
        )

        # Cache logic and main fix agent
        fix_issue_result = await fix_issue(
            repo_full_name=repo_full_name,
            query=query,
            access_token=access_token,
            snippets=ci_snippets,
            username=username,
            branch=pull_request.head.ref,
            pulls=pull_request_metadata,
            context=context,
        )
        append_to_ci_history(
            pull_request,
            [
                (
                    FixCIInput(commit_hash=commit.sha, cleaned_logs=cleaned_logs),
                    fix_issue_result,
                )
            ],
        )

        new_history = get_ci_history(pull_request)
        markdown_history = render_history_for_github_comment(pull_request, new_history)

        # Responding to user
        fix_string = (
            f"# Fixes\n > Failing CI in {create_hyperlink(commit)}\n\nIn pull request {pull_request.html_url}\n\n"
        )
        response = (
            initial_message
            + HR
            + format_results(
                fix_issue_result=fix_issue_result,
                fix_string=fix_string,
                repo=repo,
                tracking_id=tracking_id,
                is_comment=True,
            )
        )
        comment.edit(body=response + get_suffix_for_sweep_comment(tracking_id))

        response_with_revert_message = generate_revert_comment_and_format_results(
            repo, fix_issue_result, fix_string, tracking_id
        )
        response_with_revert_message = initial_message + HR + response_with_revert_message
        comment.edit(body=response_with_revert_message + get_suffix_for_sweep_comment(tracking_id))

        return fix_issue_result


async def cleanup_debug_statements(pull_request: PullRequest, tracking_id: str | None = None, force: bool = False):
    if pull_request.state != "open" and not force:
        return
    with log_to_file(tracking_id), IssueErrorHandler(
        pull_request.as_issue(),
        error_title="Error while fixing CI",
        tracking_id=tracking_id,
        do_delete=True,
    ) as monitor:
        logger.info(f"URL: {pull_request.html_url}")
        repo = pull_request.base.repo
        repo_full_name = repo.full_name
        access_token = repo._requester.auth.token
        username = get_actor_from_pull_request(pull_request)
        branch = pull_request.head.ref
        commit: Commit = pull_request.get_commits().reversed[0]

        # TODO: Check if there are any debug statements to remove

        cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_full_name, branch=branch)
        cloned_repo.safely_checkout_to_non_default_branch(branch_commit_sha=pull_request.head.sha)
        snippets = get_existing_snippets(pull_request, cloned_repo)

        initial_message = f"There are no more CI failures! I'm currently removing debug logs from attempting to fix all the CI failures."
        comment = pull_request.create_issue_comment(initial_message)
        monitor.comment = comment

        if not wildcard_match(username, FIX_CI_ALLOWLIST):
            comment.edit(
                body=f"Hey @{username}, CI auto-fix is currently not enabled for you. Please reach out to the [Sweep team](william@sweep.dev) to enable it."
                + get_suffix_for_sweep_comment(tracking_id)
            )
            return

        pull_request_metadata = generate_pull_request_metadata(pull_request)
        history_str = render_history(pull_request)
        fix_issue_result = await fix_issue(
            repo_full_name=repo_full_name,
            query="Remove debug statements add in this PR.",
            access_token=access_token,
            snippets=snippets,
            username=username,
            branch=pull_request.head.ref,
            pulls=pull_request_metadata,
            context=ChatAgentContext(
                use_case="ci",
                history=history_str,
            ),
        )

        fix_string = f"# Fixes\n > Remove debug statements in {create_hyperlink(commit)}\n\nIn pull request {pull_request.html_url}\n\n"
        response = (
            initial_message
            + HR
            + format_results(
                fix_issue_result=fix_issue_result,
                fix_string=fix_string,
                repo=repo,
                tracking_id=tracking_id,
                is_comment=True,
            )
        )
        comment.edit(body=response + get_suffix_for_sweep_comment(tracking_id))

        response_with_revert_message = generate_revert_comment_and_format_results(
            repo, fix_issue_result, fix_string, tracking_id
        )
        response_with_revert_message = initial_message + HR + response_with_revert_message
        comment.edit(body=response_with_revert_message + get_suffix_for_sweep_comment(tracking_id))

        return fix_issue_result


async def fix_ci_failures(
    pull_request: PullRequest,
    max_attempts: int = 10,
    tracking_id: str | None = None,
    force: bool = False,
):
    # TODO: add better stopping criteria (i.e. making no progress)
    results_list = []
    for i in range(max_attempts):
        fix_issue_result = await fix_ci_failures_once(pull_request, tracking_id=f"{tracking_id}-ci-{i}", force=force)
        if fix_issue_result:
            results_list.append(fix_issue_result)  # Fix attempt
        else:
            logger.info("No CI errors remaining, stopping")
            break  # Nothing else broken
        repo = get_github_repo(repo_full_name=pull_request.base.repo.full_name)
        pull_request = repo.get_pull(pull_request.number)
    # We should only run this if there's not more errors
    # if results_list:
    #     await cleanup_debug_statements(pull_request, tracking_id=f"{tracking_id}-ci-cleanup", force=force)
    return results_list
