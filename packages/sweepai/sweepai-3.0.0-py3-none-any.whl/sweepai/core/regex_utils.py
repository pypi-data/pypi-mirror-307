import re
from typing import Any


def xml_pattern(
    tags: str,
    name: str | None = None,
    add_newlines: bool = True,
    **kwargs: dict[str, str],
) -> str:
    name = name or tags
    new_lines = "\n" if add_newlines else ""
    if kwargs:
        kwargs_pattern = r"\s+" + r"\s+".join(rf"{key}=\"(?P<{value}>.*?)\"" for key, value in kwargs.items())
    else:
        kwargs_pattern = ""
    return rf"<{tags}{kwargs_pattern}>{new_lines}(?P<{name}>.*?){new_lines}</{tags}>"


tool_call_parameters = {
    "make_change": [
        "justification",
        "file_name",
        "original_code",
        "new_code",
        "replace_all",
    ],
    "create_file": ["justification", "file_name", "new_code"],
    "submit_task": ["sources", "justification", "answer"],
    "search_codebase": ["query", "question", "include_docs", "include_tests"],
    "semantic_search": ["query", "question", "include_docs", "include_tests"],
    "ripgrep": ["query"],
}


# returns a dictionary of the tool call parameters, assumes correct
def parse_function_call_parameters(tool_call_contents: str, parameters: list[str]) -> dict[str, Any]:
    tool_args = {}
    for param in parameters:
        param_regex = rf"<{param}>(?P<{param}>.*?)<\/{param}>"
        match = re.search(param_regex, tool_call_contents, re.DOTALL)
        if match:
            param_contents = match.group(param)
            tool_args[param] = param_contents
    return tool_args


# parse llm response for tool calls in xml format
def parse_function_calls(response_contents: str) -> list[dict[str, str]]:
    tool_calls = []
    # first get all tool calls
    for tool_name in tool_call_parameters.keys():
        tool_call_regex = rf"<{tool_name}>(?P<function_call>.*?)<\/{tool_name}>"
        tool_call_matches = re.finditer(tool_call_regex, response_contents, re.DOTALL)
        # now we extract its parameters
        for tool_call_match in tool_call_matches:
            tool_call_contents = tool_call_match.group("function_call")
            # get parameters based off of tool name
            parameters = tool_call_parameters[tool_name]
            tool_call = {
                "tool": tool_name,
                "arguments": parse_function_call_parameters(tool_call_contents, parameters),
                "raw_text": tool_call_match.group(0),
            }
            tool_calls.append(tool_call)
    return tool_calls


if __name__ == "__main__":
    pattern = xml_pattern("additional_changes", required="additional_changes_required")
    print(pattern)
    example_template = """\
<additional_changes required="yes">
Test
</additional_changes>"""
    print(re.match(pattern, example_template))
