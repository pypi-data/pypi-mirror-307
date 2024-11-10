import re

from sweepai.core.entities import FileChangeRequest, Snippet

# from sweepai.utils.previous_diff_utils import get_relevant_commits

BOT_ANALYSIS_SUMMARY = "bot_analysis_summary"
SNIPPET_TOKEN_BUDGET = int(150_000 * 3.5)  # 140k tokens
MAX_SNIPPETS = 15
RELEVANCE_THRESHOLD = 0.125

sandbox_error_prompt = """The following error logs were returned from `{command}`. Make changes to the current file so that it passes this CI/CD command.

```
{error_logs}
```

Edit old_code to pass the CI/CD."""

sandbox_error_prompt_test = """The following error logs were returned from `{command}`. Make changes to the current file so that it passes this CI/CD command.

```
{error_logs}
```

Edit old_code to pass the CI/CD.
1. Analyze the business logic and tests. Identify whether the failure is in the unit tests or business logic.
2a. If the business logic is correct fix the test to return the expected output.
2b. If the business logic has a bug or you are unsure, skip the failing tests with an explanation."""

GHA_PROMPT = """You're working on resolving a GitHub issue but the code changes fail the GitHub Actions.

You are trying to resolve the following GitHub issue:
<original_github_issue>
{problem_statement}
</original_github_issue>

You made some changes, but GitHub Actions failed with the following logs:
<github_actions_logs>
{github_actions_logs}
</github_actions_logs>

You have previously made the following changes. The diffs represent the current state of the file/project:
<changes_made>
{changes_made}
</changes_made>

Fix the above GitHub Actions."""

GHA_PROMPT_WITH_HISTORY = """You're working on resolving a GitHub issue but the code changes fail the GitHub Actions.

You are trying to resolve the following GitHub issue:
<original_github_issue>
{problem_statement}
</original_github_issue>

Previously the Githu Actions were failing with these logs:
<previous_github_actions_logs>
{previous_github_actions_logs}
</previous_github_actions_logs>

You made some changes to address the previous Github Action failures, but GitHub Actions are now failing with the following logs:
<current_github_actions_logs>
{current_github_actions_logs}
</current_github_actions_logs>

You have previously made the following changes. The diffs represent the current state of the file/project:
<changes_made>
{changes_made}
</changes_made>

Fix the above GitHub Actions."""

issue_sub_request_system_prompt = """You are a tech lead helping to break down a GitHub issue for an intern to solve. Identify every single one of the user's requests. Be complete. The changes should be atomic.

Guidelines:
- For well-specified issues, where all required steps are already listed, simply break down the issue.
- For less well-specified issues, where the user's requests are vague or incomplete, infer the user's intent and break down the issue accordingly. This means you will need to analyze the existing files and list out all the changes that the user is asking for.
- A sub request should correspond to a code or test change.
- A sub request should not be speculative, such as "catch any other errors", "abide by best practices" or "update any other code". Instead explicitly state the changes you would like to see.
- Tests and error handling will be run automatically in the CI/CD pipeline, so do not mention them in the sub requests.
- Topologically sort the sub requests, such that each sub request only depends on sub requests that come before it. For example, create helper functions before using them."""


def cleanup_fcrs(fcrs_string: str):
    fcrs_string = re.sub(
        r"<original_code(?: file_path=\".*?\")?(?: index=\"\d+\")?>",
        "<original_code>",
        fcrs_string,
    )
    fcrs_string = re.sub(
        r"<new_code(?: file_path=\".*?\")?(?: index=\"\d+\")?>",
        "<new_code>",
        fcrs_string,
    )
    return fcrs_string


def parse_patch_fcrs(fcr_patch_string: str):
    pattern = re.compile(
        r"""<(?P<change_type>[a-z_]+)\s+file=\"(?P<filename>[a-zA-Z0-9/\\\.\[\]\(\)\_\+\- @\{\}]*?)\"\s+index=\"(?P<index>\d+)\">(?P<instructions>.*?)\s*<\/\1>""",
        re.DOTALL,
    )
    drop_pattern = re.compile(r"<drop>(\d+?)</drop>", re.DOTALL)
    matches = []
    for match in pattern.finditer(fcr_patch_string):
        matches.append(
            (
                int(match.group("index")),
                FileChangeRequest(
                    change_type=match.group("change_type"),
                    filename=match.group("filename"),
                    instructions=match.group("instructions"),
                ),
            )
        )
    drops = [int(drop.group(1).strip()) for drop in drop_pattern.finditer(fcr_patch_string)]
    matches.sort(key=lambda x: x[0])
    return drops, [match for match in matches]


def parse_renames(renames_string: str):
    pattern = re.compile(r"<rename>(.*?)</rename>", re.DOTALL)
    old_name_pattern = re.compile(r"<old_name>(.*?)</old_name>", re.DOTALL)
    new_name_pattern = re.compile(r"<new_name>(.*?)</new_name>", re.DOTALL)
    rename_dict = {}
    for match in pattern.finditer(renames_string):
        rename_match = match.group(1)
        old_name = old_name_pattern.search(rename_match).group(1)
        if not old_name:
            continue
        new_name = new_name_pattern.search(rename_match).group(1)
        if old_name.strip() == new_name.strip():
            continue
        rename_dict[old_name.strip()] = new_name.strip()
    return rename_dict


def partition_snippets_if_test(snippets: list[Snippet], include_tests=False):
    if include_tests:
        return [snippet for snippet in snippets if "test" in snippet.file_path]
    return [snippet for snippet in snippets if "test" not in snippet.file_path]
