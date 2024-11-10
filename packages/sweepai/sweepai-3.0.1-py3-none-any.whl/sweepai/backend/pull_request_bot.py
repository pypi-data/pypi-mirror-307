import re

from loguru import logger

from sweepai.core.entities import Message
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread, call_llm
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.handlers.create_pr import INSTRUCTIONS_FOR_REVIEW
from sweepai.utils.diff import generate_diff
from sweepai.utils.str_utils import BOT_SUFFIX, extract_xml_tag, truncate_commit_message
from sweepai.utils.ticket_rendering_utils import get_branch_diff_text

commit_message_system_prompt = """Create a concise, informative commit message for GitHub from the code changes.

The output must:
1. Use an imperative tone, such as "Add", "Update", "Remove".
2. Your commit message MUST BE <50 characters long to adhere to GitHub's message length restrictions.
3. Group similar operations where applicable to avoid redundancy.
Your message must be directly related to the file changes stated. Avoid additional interpretation or detail not present in the input.

You will recieve a series of file diffs that need to be described in a short commit message.

Return your commit message in the following xml format:

<thinking>
1. Explain what happened in the file diffs, focusing on the lines added and removed. 
2. Try to identify the ideal commit message that reflects the changes made, whether the changes are substantial or minor. Remember to keep the message concise and clear, focusing on the file operations performed. Again, the commit message must be less than 50 characters long.
</thinking>

<commit_message>
short and concise description of the file diffs for a GitHub commit, not exceeding 50 characters
</commit_message>"""

commit_message_user_prompt = """Below are a series of file diffs to create a github commit message for:

{file_diffs}"""

pr_summary_system_prompt = """You are a helpful, excellent developer who is creating a pull request for a feature or bug fix. You need to write a pull request description that the changes in this pull request. You will always describe changes from higher to lower level, describing the purpose and value and then the details of the changes."""

pr_summary_prompt = """\
Write a pull request description that reflects all changes in this pull request. Here is the issue that this pull request is addressing:
<github_issue>
{issue}
</github_issue>

Here are the changes:
<diffs>
{diffs}
</diffs>

Format your response using the following XML tags:
<pr_title>
Title of the pull request.
</pr_title>
<pr_description>
# Purpose
Briefly describe the purpose of this pull request.
# Description
Description of the functional changes made in this pull request.
# Summary
Concise bulleted description of the pull request. Markdown format `variables`, `files`, and `directories` like this.
</pr_description>"""

GHA_SUMMARY_START = "<!-- GHA_SUMMARY_START -->"
GHA_SUMMARY_END = "<!-- GHA_SUMMARY_END -->"
MAX_COMMIT_MESSAGE_LENGTH = 64


class PRSummaryBot(Thread):
    # get commit message based on the patches
    # if previous patches are passed in then generate the incremental commit message
    def get_commit_message(
        self,
        modify_files_dict: dict[str, dict[str, str]],
        renames_dict: dict[str, str] = {},
        previous_modify_files_dict: dict[str, dict[str, str]] = {},
    ):
        self.messages = [
            Message(
                role="system",
                content=commit_message_system_prompt,
            )
        ]
        file_diffs = ""
        if not previous_modify_files_dict:
            for file_name, file_data in modify_files_dict.items():
                file_diff = generate_diff(file_data["original_contents"], file_data["contents"])
                file_diffs += f"<file_diffs file='{file_name}'>\n{file_diff}\n</file_diffs>"
        else:
            if modify_files_dict:
                for file_name, file_data in modify_files_dict.items():
                    # use incremental diff, compare against previous file data
                    if file_name in previous_modify_files_dict:
                        previous_file_data = previous_modify_files_dict[file_name]
                        file_diff = generate_diff(previous_file_data["contents"], file_data["contents"])
                    else:
                        # use diff compare against original file data
                        file_diff = generate_diff(file_data["original_contents"], file_data["contents"])
                    file_diffs += f"<file_diffs file='{file_name}'>\n{file_diff}\n</file_diffs>"
        for file_name, new_file_name in renames_dict.items():
            file_diff = f"File {file_name} was renamed to {new_file_name}"
            file_diffs += f"<file_diffs file='{file_name}'>\n{file_diff}\n</file_diffs>"

        if not file_diffs.strip():
            return "No changes were made"
        formatted_user_prompt = commit_message_user_prompt.format(file_diffs=file_diffs)
        commit_message_response = self.chat(
            content=formatted_user_prompt,
            model="claude-3-haiku-20240307",
        )
        commit_message = self.extract_commit_message(commit_message_response)
        if len(commit_message) > 50:
            shorter_commit_prompt = f'Your commit message is too long and was truncated to "{commit_message[:50]}".\nWrite a shorter commit message than "{commit_message}" that is still coherent.\n<commit_message>'
            shorter_commit_message_response = self.chat(
                content=shorter_commit_prompt,
                model="claude-3-haiku-20240307",
            )
            commit_message = self.extract_commit_message(shorter_commit_message_response)
        if not commit_message:
            logger.error("Failed to extract commit message from response.")
            commit_message = f"feat: Updated {len(modify_files_dict or [])} files"[:50]
        return commit_message

    def extract_commit_message(self, response: str):
        commit_message = ""
        commit_message_pattern = r"<commit_message>(?P<commit_message>.*?)</commit_message>"
        commit_message_match = re.search(commit_message_pattern, response, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group("commit_message").strip()
        return commit_message

    # pylint: disable=E0213
    def get_pull_request_summary(
        problem_statement,
        issue_number,
        repo,
        overrided_branch_name,
        pull_request,
        pr_changes,
    ):
        # change the body here
        diff_text = get_branch_diff_text(
            repo=repo,
            branch=pull_request.branch_name,
            base_branch=overrided_branch_name,
        )
        # attempt to generate description 3 times
        for attempt in [0, 1, 2]:
            pr_desc_response = call_llm(
                system_prompt=pr_summary_system_prompt,
                user_prompt=pr_summary_prompt,
                params={
                    "issue": problem_statement,
                    "diffs": diff_text,
                },
            )
            pr_title_matches = re.search(r"<pr_title>\n(.*?)\n</pr_title>", pr_desc_response, re.DOTALL)
            pr_desc_matches = re.search(
                r"<pr_description>\n(.*?)\n</pr_description>",
                pr_desc_response,
                re.DOTALL,
            )
            if pr_desc_matches is None or pr_title_matches is None and attempt == 2:
                return pr_changes
            else:
                new_description = pr_desc_matches.group(1)
                new_title = pr_title_matches.group(1)
                pr_changes.title = f"Sweep: {new_title}"
                pr_changes.body = (
                    f"{new_description}\n\nFixes"
                    f" #{issue_number}.\n\n---\n{GHA_SUMMARY_START}{GHA_SUMMARY_END}\n\n{INSTRUCTIONS_FOR_REVIEW}{BOT_SUFFIX}"
                )
        return pr_changes


pr_summary_for_chat_system_prompt = """You are a helpful, excellent developer who is creating a pull request for a feature or bug fix. You need to write a pull request description that the changes in this pull request. You will always describe changes from higher to lower level, describing the purpose and value and then the details of the changes."""

pr_summary_for_chat_prompt = """\
Write a pull request description that reflects all changes in this pull request, for the repository {repo_name}.

Here is the conversation history that led to the changes:
<conversation>
{conversation}
</conversation>

<diff>
{diffs}
</diff>{pr_template}

Format your response using the following XML tags:

<pr_title>
Title of the pull request.
</pr_title>
<pr_description>
# Purpose
Briefly describe the purpose of this pull request.
# Description
Description of the functional changes made in this pull request.
# Summary
Concise bulleted description of the pull request. Markdown format `variables`, `files`, and `directories` like this.
</pr_description>"""


def get_pr_summary_for_chat(
    repo_name: str,
    modify_files_dict: FileModificationState,
    pr_template_string: str = "",
):
    diff_text = "\n\n".join(
        [
            f"{file_name}:\n" + generate_diff(file_contents.original_contents, file_contents.new_contents)
            for file_name, file_contents in modify_files_dict.files.items()
        ]
    )
    response = call_llm(
        system_prompt=pr_summary_for_chat_system_prompt,
        user_prompt=pr_summary_for_chat_prompt,
        params={
            "repo_name": repo_name,
            "diffs": diff_text,
            "pr_template": (
                f"\n\nHere is the repo's PR template:\n<pr_template>\n{pr_template_string}\n</pr_template>"
                if pr_template_string
                else ""
            ),
        },
        model=LATEST_CLAUDE_MODEL,
    )
    title = extract_xml_tag(response, "pr_title")
    description = extract_xml_tag(response, "pr_description")
    return title, description


commit_message_chat_system_prompt = """You are a helpful, excellent developer who is creating a commit message for a feature or bug fix. You need to write a commit message for the changes in this diff."""

commit_message_chat_prompt = """\
You are tasked with writing a commit message based the diff of the changes made to relevant files. Your goal is to accurately summarize the changes and provide a concise, informative commit message.

Carefully analyze the diff of the changes:

<diff>
{diffs}
</diff>

Format your response using the following XML tags:

<commit_message>
Short and concise description of the file diffs for a GitHub commit, not exceeding {MAX_COMMIT_MESSAGE_LENGTH} characters
</commit_message>
"""


def get_commit_message_for_diff(modify_files_dict: FileModificationState):
    diff_text = "\n\n".join(
        [
            f"{file_name}:\n" + generate_diff(file_contents.original_contents, file_contents.new_contents)
            for file_name, file_contents in modify_files_dict.files.items()
        ]
    )
    response = call_llm(
        system_prompt=commit_message_chat_system_prompt,
        user_prompt=commit_message_chat_prompt,
        params={
            "diffs": diff_text,
            "MAX_COMMIT_MESSAGE_LENGTH": MAX_COMMIT_MESSAGE_LENGTH,
        },
    )
    commit_message = extract_xml_tag(response, "commit_message") or (
        f"Edited " + ", ".join(list(modify_files_dict.files.keys()))
    )
    commit_message = truncate_commit_message(commit_message)
    return commit_message
