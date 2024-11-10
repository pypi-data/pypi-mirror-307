from sweepai.core.llm.chat import Thread, continuous_llm_calls
from sweepai.utils.format_utils import Prompt

system_message = "You are a helpful assistant that will help determine if a set of files is sufficient for answering a technical question about a codebase, or if additional searching in the codebase is required."

user_message_prompt = Prompt(
    """
Here are your relevant files:
<relevant_files>
{{ snippets|render_snippets }}
</relevant_files>

Here is the user's question:
<user_request>
{{ question }}
</user_request>

Respond in the following XML format:
<analysis>

Given a set of code snippets and a question about a codebase, analyze the snippets to determine if there is sufficient information to answer the question. Provide your analysis in the following XML format:

<format>
<analysis>
a. Break down the user's question to determine what information you need.
b. For each provided snippet that is relevant to the question:
    1. [List each relevant code symbol defined in this snippet. Then, for each symbol, give an extremely detailed explanation of what information it contains. If it is a complex function or class, give an extremely detailed step by step explanation of how it works.]
</analysis>
<relevant_snippets>
<snippet>path/to/file.py:1-10</snippet>
<snippet>path/to/another/file.py:12-20</snippet>
<!-- Add more snippet tags as needed -->
</relevant_snippets>
<missing_information>
<item>[Describe a piece of missing information]</item>
<item>[Describe another piece of missing information]</item>
<!-- Add more item tags as needed -->
</missing_information>
<conclusion>
[For each missing piece of information, think critically about whether it is necessary to answer the question or present in the snippets.]
</conclusion>
<sufficient_information>[true/false]</sufficient_information>
<confidence_level>[0-100]</confidence_level>
</format>
"""
)


def use_instant_reply(question: str, snippets: list[str]):
    thread = Thread.from_system_message_string(system_message)
    user_message = user_message_prompt.render(question=question, snippets=snippets)

    response = continuous_llm_calls(
        username="anonymous",
        thread=thread,
        content=user_message,
        model="claude-3-opus-20240229",  # Sonnet has context issues
    )

    return "<sufficient_information>true</sufficient_information>" in response
