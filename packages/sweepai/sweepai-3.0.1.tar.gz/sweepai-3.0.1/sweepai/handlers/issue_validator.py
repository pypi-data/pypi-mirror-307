import re

from sweepai.config.server import DEV
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread

# TODO: add to on_ticket.py

# BAD ISSUES
# - Renaming a class or file or function or variable
# - Deleting a file or dead code or class
# - Attaching files - sweep cannot access urls such as documents or pdf files. For pdfs, say it's not supported rn. Same for screenshots.
# - vague requests. Sweep will reject poorly specified issues.
# - versioning eg mongo 3 to mongo 7 or python 2 to python 3. maybe we can set a limit for these like one file is fine but not codebase wide refactors
# -
# GOOD ISSUES
# - Adding a unit test
# - Well specified task

issue_validator_instructions_prompt = """# Instructions for Evaluating Issues for Sweep

You are an AI assistant tasked with evaluating GitHub issues to determine if they are suitable for Sweep, an automated code modification tool. Your goal is to assess if the issue is clear, actionable, and within Sweep's capabilities.

## Sweep's Capabilities

Sweep can:
- Access and search the entire codebase to find relevant code
- Make targeted code changes to fix bugs or add features 
- Write unit tests well. If the task relates to unit tests, you should usually pass it.
- Refactor small to medium sized components
- Update API usage across a codebase
- Read GitHub Action logs

Sweep works best with issues that:
- Have clear, specific instructions
- Involve changes to <10 files and <2000 lines of code
- Don't require external resources or command line operations

Reject issues that:
- Can be easily done with a basic find-and-replace operation or a rename tool in the IDE.
- Would likely require huge changes, like "migrate my codebase from Python to Rust". This task is too broad for Sweep.

## Examples

Good issues for Sweep:
- "Fix the bug in utils.py where the sort_items() function is not handling empty lists correctly"
- "Add input validation to the create_user() function in users/views.py to check that the email is valid"
- "Refactor the ProductList component in src/components/ProductList.js to use hooks instead of class components"

Issues that may need clarification:
- "Update the entire codebase to Python 3.9" (too broad)
- "Fix all the failing tests" (needs more specifics)
- "Improve performance" (needs concrete steps)

Bad issues for Sweep:
- "Rename the class User to UserDetails in the file users/models.py"
- "Delete the entire utils folder"

## Your Task

For each issue, analyze whether it's suitable for Sweep. If it's unclear or outside Sweep's capabilities, suggest how it could be improved.

Respond in this format:

<thinking>
Provide your analysis here. Consider:
- Is the issue clear and specific?
- Is it within Sweep's capabilities?
- If not, how could it be improved?
</thinking>

<pass>True or False</pass>

If False, respond to the user:
<response_to_user>
1. Explain what you've detected that makes the issue unsuitable for Sweep.
2. Offer suggestions to improve it. Use a friendly but concise tone.
</response_to_user>"""

issue_validator_system_prompt = """You are an AI assistant tasked with determining whether an issue should be passed on to be handled by Sweep, an AI-powered software engineer."""

issue_validator_user_prompt = (
    """<issue>
{issue}
</issue>\n\n"""
    + issue_validator_instructions_prompt
)


def validate_issue(issue: str) -> tuple[bool, str]:
    """
    Validate the issue and provide instructions for overriding if it fails.
    """
    if DEV:
        return True, ""
    thread: Thread = Thread.from_system_message_string(
        prompt_string=issue_validator_system_prompt,
    )

    response = thread.chat(
        issue_validator_user_prompt.format(issue=issue),
        model=LATEST_CLAUDE_MODEL,
        temperature=0.0,
    )

    if "<pass>False</pass>" in response:
        pattern = "<response_to_user>(.*)</response_to_user>"
        validation_message = re.search(pattern, response, re.DOTALL).group(1).strip()
        override_instructions = "\n\n> [!TIP]\n> If you would like to proceed despite this, you can override the validation by adding the text `OVERRIDE_ISSUE_VALIDATION` anywhere in your issue description."
        return False, validation_message + override_instructions
    return True, ""


if __name__ == "__main__":
    print(validate_issue("Rename the method get_jwt in sweepai/core/github_utils.py to get_jwt_2"))
