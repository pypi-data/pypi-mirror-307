import re

from github.Repository import Repository

from sweepai.dataclasses.code_change_stream_state import CodeChangeStreamState
from sweepai.dataclasses.fix_issue_result import FixIssueResult
from sweepai.utils.diff import generate_diff
from sweepai.utils.str_utils import (
    get_xml_parsing_regex,
    markdown_list,
    ordered_dedup,
    strip_triple_quotes,
)
from sweepai.utils.ticket_rendering_utils import (
    SWEEPING_PNG,
    get_suffix_for_sweep_comment,
)

RESPONSE_FORMAT = """## Search Results

{snippets}

## Response

{response}

Continue the conversation with Sweep here: {html_url}."""

WARNING_FORMAT = """> [!WARNING]
> {warning}"""


def extract_diff_patches(fix_issue_result: FixIssueResult) -> list[str]:
    messages = fix_issue_result.messages
    pull_request = fix_issue_result.pull_request_data
    last_message_content = messages[-1].content if not pull_request else messages[-2].content
    results = ""
    matches = re.finditer(CodeChangeStreamState.code_change_partial_regex, last_message_content, re.DOTALL)
    for match_ in matches:
        raw_diff = generate_diff(
            strip_triple_quotes(match_["originalCode"] or ""),
            strip_triple_quotes(match_["newCode"] or ""),
        ).strip("\n")
        diff = f"#### `{match_['filePath']}`\n```diff\n{raw_diff}\n```\n\n"
        results += diff
    return results


def format_results_body(fix_issue_result: FixIssueResult):
    messages = fix_issue_result.messages
    pull_request = fix_issue_result.pull_request_data

    last_message_content = messages[-1].content if not pull_request else messages[-2].content

    matches = re.finditer(CodeChangeStreamState.code_change_partial_regex, last_message_content, re.DOTALL)
    for match_ in matches:
        raw_diff = generate_diff(
            strip_triple_quotes(match_["originalCode"] or ""),
            strip_triple_quotes(match_["newCode"] or ""),
        ).strip("\n")
        diff = f"#### `{match_['filePath']}`\n```diff\n{raw_diff}\n```"
        last_message_content = last_message_content.replace(match_.group(0), diff)

    matches = re.finditer(
        get_xml_parsing_regex("file_path") + "\n+" + get_xml_parsing_regex("new_code"),
        last_message_content,
        re.DOTALL,
    )
    for match_ in matches:
        file_path = match_.group("file_path")
        new_code = strip_triple_quotes(match_.group("new_code"))
        ext = file_path.split(".")[-1] if "." in file_path else ""
        replacement = f"#### `{file_path}`\n```{ext}\n{new_code}\n```"
        last_message_content = last_message_content.replace(match_.group(0), replacement)

    file_list = ordered_dedup([snippet.file_path for snippet in fix_issue_result.snippets])
    sweep_response = RESPONSE_FORMAT.format(
        snippets=markdown_list(file_list),
        response=last_message_content,
        html_url=fix_issue_result.frontend_url,
    )
    return sweep_response


def format_results(
    fix_issue_result: FixIssueResult,
    fix_string: str,
    repo: Repository,
    tracking_id: str | None = None,
    is_comment: bool = False,
):
    pr_url = fix_issue_result.pull_request_data.html_url if fix_issue_result.pull_request_data else None

    sweep_response = format_results_body(fix_issue_result)
    sweep_response = SWEEPING_PNG + sweep_response

    if fix_issue_result.pull_request_data:
        pr_number = fix_issue_result.pull_request_data.number
        if is_comment:
            sweep_response = (
                f"""<div align='center'><h1 align="center">🚀 I've committed these changes to your branch via this PR! <a href="{pr_url}">#{pr_number}</a></h1></div>
<div align='center'></div>\n\n"""
                + sweep_response
            )
        else:
            header = f"""<div align='center'><h1 align="center">🚀 Here's the PR! <a href="{pr_url}">#{pr_number}</a></h1></div>
<div align='center'></div>\n\n"""
            sweep_response = header + sweep_response
            # this is only for on_ticket
            github_pull_request = repo.get_pull(pr_number)
            final_pull_request_body = (
                fix_issue_result.pull_request_data.body
                + f"\n\n{fix_string.strip()}. Continue the conversation here: {fix_issue_result.frontend_url}."
                + '\n\nTo have Sweep make further changes, please add a comment to this PR starting with "Sweep:".'
            )
            # This is a side effect and does not have an impact on the response
            github_pull_request.edit(
                body=final_pull_request_body + get_suffix_for_sweep_comment(tracking_id=tracking_id)
            )
    return sweep_response
