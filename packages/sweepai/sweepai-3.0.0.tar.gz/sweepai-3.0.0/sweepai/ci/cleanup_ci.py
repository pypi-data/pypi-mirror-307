from sweepai.core.entities import Message
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread, continuous_llm_calls
from sweepai.utils.cache import create_cache
from sweepai.utils.format_utils import Prompt
from sweepai.utils.str_utils import safe_extract_xml_tag, tail

cache = create_cache()

ci_cleanup_system_prompt = (
    """You are an expert Devops engineer that extracts lines from failing Continuous Integration (CI) systems."""
)

ci_cleanup_user_prompt = Prompt(
    """# Task:
Your job is to extract ALL logs from the CI error logs that contain relevant information to fixing the issue.

{{ pulls_message }}


<error_logs>
{{ error_logs }}
</error_logs>

# Instructions

Copy the all of the important lines from this CI/CD run. Don't leave out any information that helps solve the failing CI/CD. 
If there is a certain type of error such as a missing dependency, include all specific instances of (file path x error) so all of the instances can be fixed.
If the exact same error occurs multiple times in one file, only include the first instance of the error. But if the error occurs in multiple files, include all files where the error occurs.

# Format:
Respond in this format:

<log_extraction_analysis>
1. Identify the main error(s).
2. Identify any patterns or recurring problems observed.
3. Then, identify all irrelevant information.
4. Indicate if any debug log statements were added to the error logs.
</log_extraction_analysis>

<most_important_lines>
[First, copy the CI command that failed.]

[Second, copy the important logs here.]
</most_important_lines>"""
)


def clean_ci_logs(
    username: str,
    error_logs: str,
    pulls_message: str,
    max_lines: int = 1000,
) -> str:
    # Keep only the last 1000 lines of error_logs
    error_logs = tail(error_logs, max_lines)
    thread = Thread(
        messages=[
            Message(role="system", content=ci_cleanup_system_prompt),
        ]
    )
    content = ci_cleanup_user_prompt.render(
        error_logs=error_logs,
        pulls_message=pulls_message,
    )
    response = continuous_llm_calls(
        username=username,
        thread=thread,
        content=content,
        stop_sequences=["</most_important_lines>"],
        model=LATEST_CLAUDE_MODEL,
    )
    return safe_extract_xml_tag(response, "most_important_lines")


if __name__ == "__main__":
    # Testing the prompt
    prompt = ci_cleanup_user_prompt.render(error_logs="test", pulls_message="pull")
    assert prompt.startswith("# Task:")
    assert "<error_logs>" in prompt