# ensure that all additional_messages are 32768 characters at most, if not split them
import os
import re
import subprocess
import textwrap
from dataclasses import dataclass
from itertools import zip_longest
from typing import Callable, get_type_hints

from loguru import logger

from sweepai.config.client import SweepConfig
from sweepai.core.entities import Message, Snippet
from sweepai.core.github_utils import ClonedRepo, MockClonedRepo
from sweepai.core.llm.chat import Thread, continuous_llm_calls
from sweepai.core.llm.convert_openai_anthropic import AnthropicFunctionCall
from sweepai.core.regex_utils import parse_function_call_parameters
from sweepai.dataclasses.llm_state import LLMState
from sweepai.modify.modify_utils import english_join
from sweepai.modify.validate.code_validators import get_parser
from sweepai.search.agent.code_tree import CodeTree
from sweepai.search.agent.ripgrep_utils import cleaned_rg_output
from sweepai.search.query.ticket_utils import prep_snippets
from sweepai.utils.str_utils import find_filenames
from sweepai.utils.streamable_functions import StreamableFunction, streamable

"""
ENTITIES AND ABSTRACTIONS LOGIC FOR TOOL CALLING START
"""


@dataclass
class Parameter:
    description: str
    optional: bool = False


@dataclass
class Tool:
    name: str
    parameters: list[str]
    parameters_explanation: dict[str, str]
    parameters_optional: dict[str, bool]
    function: Callable[..., str] | StreamableFunction[..., str, str]
    description: str = ""

    def get_xml(self, include_function_call_tags: bool = True, include_description: bool = True):
        parameters_xml = "\n".join(
            f"<{parameter}>\n{self.parameters_explanation[parameter]}\n</{parameter}>" for parameter in self.parameters
        )
        function_xml = f"""<{self.name}>
{parameters_xml}
</{self.name}>"""
        if include_function_call_tags:
            function_xml = f"<function_call>\n{function_xml}\n</function_call>"
        if include_description and self.description:
            function_xml = f"{self.name} - {self.description}\n\n{function_xml}"
        return function_xml

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def stream(self, *args, **kwargs):
        return self.function.stream(*args, **kwargs)


def tool(**kwargs):
    """Docstrings are automatically dedented."""

    def decorator(func):
        func_ = func._stream if isinstance(func, StreamableFunction) else func
        type_hints = get_type_hints(func_)
        func_params = func_.__code__.co_varnames[: func_.__code__.co_argcount]
        parameters_explanation = {}
        parameters = []
        parameters_optional = {}
        for parameter in func_params:
            if isinstance(type_hints.get(parameter), Parameter):
                parameters.append(parameter)
                parameters_explanation[parameter] = type_hints[parameter].description
                parameters_optional[parameter] = type_hints[parameter].optional
        docstrings = textwrap.dedent(func_.__doc__ or "").strip()
        return Tool(
            name=func_.__name__ or kwargs.get("name", ""),
            parameters=parameters,
            parameters_explanation=parameters_explanation,
            parameters_optional=parameters_optional,
            function=func,
            description=docstrings,
        )

    return decorator


"""
ENTITIES AND ABSTRACTIONS LOGIC FOR TOOL CALLING END, START OF FUNCTION PARSING LOGIC
"""


def parse_function_calls(response_contents: str, tools: list[Tool]) -> list[dict[str, str]]:
    """
    Parse all tool calls made in the order they appear in the response contents.
    """
    tool_call_parameters = {tool.name: tool.parameters for tool in tools}
    tool_calls = []

    # Create a regex pattern that matches all tool calls
    all_tool_names = "|".join(re.escape(name) for name in tool_call_parameters.keys())
    all_tool_calls_regex = rf"<({all_tool_names})>(?P<function_call>.*?)<\/\1>"

    # Find all tool calls in the order they appear
    all_matches = list(re.finditer(all_tool_calls_regex, response_contents, re.DOTALL))

    # Process matches in the order they were found
    for match in all_matches:
        tool_name = match.group(1)
        tool_call_contents = match.group("function_call")
        parameters = tool_call_parameters[tool_name]
        tool_call = {
            "tool": tool_name,
            "arguments": parse_function_call_parameters(tool_call_contents, parameters),
            "raw_text": match.group(0),  # include the full match
        }
        tool_calls.append(tool_call)

    return tool_calls


def validate_and_parse_function_call(
    function_calls_string: str, thread: Thread, tools: list[Tool]
) -> AnthropicFunctionCall:
    function_calls = parse_function_calls(function_calls_string.strip("\n") + "\n</function_call>", tools)
    if len(function_calls) > 0:
        function_calls[0] = AnthropicFunctionCall(
            function_name=function_calls[0]["tool"],
            function_parameters=function_calls[0]["arguments"],
            raw_text=function_calls[0]["raw_text"],
        )
        if "<function_call>" in function_calls_string:
            thread.messages[-1].content = thread.messages[-1].content.rstrip("\n") + "\n</function_call>"
    return function_calls[0] if len(function_calls) > 0 else None


def validate_and_parse_multi_function_calls(
    function_calls_string: str, thread: Thread, tools: list[Tool]
) -> AnthropicFunctionCall:
    function_calls = parse_function_calls(function_calls_string.strip("\n") + "\n</function_call>", tools)
    for index, function_call in enumerate(function_calls):
        function_calls[index] = AnthropicFunctionCall(
            function_name=function_call["tool"],
            function_parameters=function_call["arguments"],
            raw_text=function_call["raw_text"],
        )
        if function_calls_string.count("<function_call>") < function_calls_string.count("</function_call>"):
            thread.messages[-1].content = thread.messages[-1].content.rstrip("\n") + "\n</function_call>"
    return function_calls


"""
END OF FUNCTION PARSING LOGIC, START OF TOOL CALL HANDLING
"""


@streamable
def handle_function_call(function_call: AnthropicFunctionCall, tools: list[Tool], **kwargs):
    # Use next() instead
    for tool in tools:
        if function_call.function_name == tool.name:
            for param in tool.parameters:
                if param not in function_call.function_parameters and not tool.parameters_optional[param]:
                    return f"ERROR\n\nThe {param} parameter is missing from the function call."
            function_kwargs = {
                **{k: v.strip() if isinstance(v, str) else v for k, v in function_call.function_parameters.items()},
            }
            for param in tool.parameters:
                if param not in function_call.function_parameters:
                    function_kwargs[param] = ""
            function = tool.function._stream if isinstance(tool.function, StreamableFunction) else tool.function
            param_names = function.__code__.co_varnames[: function.__code__.co_argcount]
            for kwarg in kwargs:
                if kwarg in param_names:
                    function_kwargs[kwarg] = kwargs[kwarg]
            if isinstance(tool.function, StreamableFunction):
                for result in tool.function._stream(**function_kwargs):
                    yield result
            else:
                yield tool.function(**function_kwargs)
            break
    else:
        yield "ERROR\n\nInvalid tool name. Must be one of the following: " + ", ".join([tool.name for tool in tools])


@streamable
def handle_multiple_function_calls(function_calls: list[AnthropicFunctionCall], tools: list[Tool], **kwargs) -> dict:
    """
    Handles multiple function calls and returns the results.
    On failure, return immediately without running the rest of the function calls.
    """
    results = ["ERROR" for _ in function_calls]
    did_error = False
    for index, function_call in enumerate(function_calls):
        for result in handle_function_call.stream(function_call, tools, **kwargs):
            results[index] = result
            if result.startswith("ERROR"):
                did_error = True
            yield {
                "status": "success" if not did_error else "error",
                "results": results,
            }

    yield {"status": "success" if not did_error else "error", "results": results}


NO_TOOL_CALL_PROMPT = """FAILURE
Your last function call was incorrectly formatted.

Make sure you provide XML tags for function_call, tool_name and parameters for all function calls. Check the examples section for reference.

Resolve this error by following these steps:
1. In a scratchpad, list the tag name of each XML blocks of your last assistant message.
2. Based on the XML blocks and the contents, determine the last function call you were trying to make.
3. Describe why your last function call was incorrectly formatted.
4. Finally, re-invoke your last function call with the corrected format, with the contents copied over.

Remember to use the following format for your function calls:
<function_calls>
<function_call>
<TOOL_NAME>
<PARAMETER_NAME>PARAMETER_VALUE</PARAMETER_NAME>
...
</TOOL_NAME>
</function_call>
[other function calls]
</function_calls>

The tools available are {tools}."""  # Updated format for explaining how to use funcction calls


def format_multi_function_call_results(
    username: str,
    thread: Thread,
    function_calls_response: dict,
    function_calls: list[AnthropicFunctionCall],
):
    # TODO: use django templates
    formatted_results = ""
    summary_string = ""
    # if no function calls were made, return the user message
    if not function_calls:
        return function_calls_response.get("results", ["No recognized function calls were made!"])[0]
    for index, (function_call, function_call_response) in enumerate(
        zip_longest(function_calls, function_calls_response.get("results", []))
    ):
        # print normally if the function call was successful or if it succeded before the failed call
        if function_call_response is None:
            continue
        if function_calls_response.get("status", "") == "success":
            tool_name = function_call.function_name
            formatted_results += (
                f"<{tool_name}_results>\nYou called the tool {tool_name} with the following parameters:\n\n"
            )
            for param, value in function_call.function_parameters.items():
                if param in function_call.function_parameters:
                    formatted_results += f"<{param}>{value}</{param}>\n"
            # function_call_results = function_calls_response["results"][index]
            formatted_results += (
                f"The tool was used with the following output:\n\n{function_call_response}\n</{tool_name}_results>\n\n"
            )
            # handle the case where the function call failed - update last message

            summary_string += f"\n\n{index}. You called the tool {tool_name} with the following parameters:\n\n"
            for param, value in function_call.function_parameters.items():
                if param in function_call.function_parameters:
                    summary_string += f"{param}: {value}\n"
            summary_string += (
                f"Which was successful, with an output containing {len(function_call_response.splitlines())} lines."
            )
        elif function_calls_response.get("status", "") == "error":
            tool_name = function_call.function_name
            formatted_results += (
                f"<{tool_name}_results>\nYou called the tool {tool_name} with the following parameters:\n\n"
            )
            for param, value in function_call.function_parameters.items():
                if param in function_call.function_parameters:
                    formatted_results += f"{param}: {value}\n"
            # error_message = function_calls_response["message"]
            formatted_results += (
                f"BUT IT FAILED with the following error message:\n{function_call_response}\n</{tool_name}_result>\n\n"
            )
            # update the last message to remove all following function calls after this one
            thread.messages[-1].content = thread.messages[-1].content.split(function_call.raw_text)[0]

            summary_string += f"\n\n{index}. You called the tool {tool_name} with the following parameters:\n\n"
            for param, value in function_call.function_parameters.items():
                if param in function_call.function_parameters:
                    summary_string += f"{param}: {value}\n"
            summary_string += "Which failed."
    formatted_results = formatted_results.strip() + f"\n\n<summary>\n{summary_string.strip()}\n</summary>\n"
    return formatted_results


@streamable
def get_multi_function_calls(
    username: str,
    thread: Thread,
    user_message: str,
    tools: list[Tool],
    llm_kwargs: dict,
    no_tool_call_prompt: str = NO_TOOL_CALL_PROMPT,
    **kwargs,
):
    """
    Get's and handles multiple tool calls per response, returning all function calls and outputs.
    """
    response = ""
    for response in continuous_llm_calls.stream(
        username,
        thread,
        content=user_message,
        stop_sequences=["</function_calls>"],
        **llm_kwargs,
    ):
        # TODO: check for duplicate function calls
        function_calls = validate_and_parse_multi_function_calls(response, thread, tools)
        if "<function_calls>" in response:
            yield response.split("<function_calls>")[0], {}, function_calls
        else:
            yield response.split("<function_call>")[0], {}, function_calls

    function_calls = validate_and_parse_multi_function_calls(response, thread, tools)

    if not function_calls:
        logger.warning("[YELLOW] No function calls were found in the response.")
        user_message = no_tool_call_prompt.format(tools=english_join([tool.name for tool in tools]))
        function_calls_response = {"status": "success", "results": [user_message]}
    else:
        for function_calls_response in handle_multiple_function_calls.stream(function_calls, tools, **kwargs):
            yield response.split("<function_calls>")[0], function_calls_response, function_calls

    if "<function_calls>" in response:
        yield response.split("<function_calls>")[0], function_calls_response, function_calls
    else:
        yield response.split("<function_call>")[0], function_calls_response, function_calls
    return function_calls_response, function_calls


"""
END OF TOOL CALL HANDLING
"""

"""
COMMON PROMPTS
"""
DUPLICATE_QUESTION_MESSAGE = """You've already asked this question: {question}

Please ask a different question. If you can not find the answer in the search results, you need to ask more specific questions or ask questions about tangentially related topics. For example, if you find that a certain functionality is handled in another utilty module, you may need to search for that utility module to find the relevant information."""

SEARCH_RESULT_INSTRUCTIONS = """

First, think step-by-step in a scratchpad to analyze the search results and determine whether the answers provided here are sufficient or if there are additional relevant modules that we may need, such as referenced utility files, docs or tests.

Then, determine if the results are sufficient to answer the user's request:

<request>
{request}
</request>

Option A: Make additional search queries

If the search results are insufficient, you need to ask more specific questions or ask questions about tangentially related topics. For example, if you find that a certain functionality is handled in another utilty module, you may need to search for that utility module to find the relevant information. Keep in mind that you have already asked the following questions, so do not ask them again:

<previously_searched_queries>
{visited_questions}
</previously_searched_queries>

Instead, search for more specific, targetted search queries by analyzing the newly retrieved information. Think step-by-step to construct these better search queries.

Alternatively, if you have found a file that seems relevant but you would like to see the rest of the file, you can use the `access_file` tool to access the contents of the file.

Option B: Submit the task

Otherwise, if you have found all the relevant information to answer the user's request, submit the task using submit_task. If you submit, ensure that the <answer> includes relevant implementations, usages and examples of code wherever possible. Ensure that the <sources> section is MINIMAL and only includes all files you reference in your answer, and is correctly formatted, with each line contains a file path, start line, end line, and justification like in the example in the instructions.

If you have exhausted all search options and still have not found the answer, you can submit an answer with everything you've searched for and found, clarifying that you can not find the answer.

Remember to use the valid function call format for either options."""

RIPGREP_SEARCH_RESULT_INSTRUCTIONS = """

Keep in mind you've already made these previous ripgrep queries, so you shouldn't make them again:
<previously_searched_queries>
{visited_questions}
</previously_searched_queries>"""

DUPLICATE_RIPGREP_MESSAGE = """You've already ran ripgrep on this query: {question}

Please ask a different question. If you can not find the answer in the search results, you need to make a broader ripgrep query."""

"""
COMMON TOOLS
"""


def post_filter_ripgrep_results(
    results: str,
    max_line_length: int = 300,
):
    output = ""
    for line in results.splitlines():
        if len(line) < 300:
            output += line + "\n"
        else:
            output += line[:300] + f"... (omitted {len(line) - 300} characters)\n"
    return output.strip("\n")


"""
TODO: add support for ripgrep cot block
"""


@tool()
def ripgrep(
    justification: Parameter("Justify why this ripgrep query is necessary, and why your search query must exist in the codebase."),  # type: ignore
    query: Parameter("The keyword to search for in the codebase. This will match against all file contents in the repository."),  # type: ignore
    cloned_repo: ClonedRepo,
    llm_state: LLMState,
):
    """
    Search for specific code symbols in the codebase. You should use this instead of `vector_search` if you know the name of the keyword you are searching for, such as for specific user-facing copy or the name of an endpoint. To find all usages of a function or class, you should use `view_entity` instead.

    You may use regex to search through file contents or directly search for a keyword:

    Examples:
    To find where the button containing the user-facing copy "View all" is defined: view all
    To find where the error message "Invalid email" is defined: invalid email

    If you do not see an entity in context, use vector search instead.

    Bad examples:

    To search for where utility functions for push notifications are defined: push_notifications
    Unless you see an invocation of push_notifications, do not use this. It could be called something else like notificationServices.push.

    To search for usages of authentication: authentication
    This is too vague, and the repository might refer to authentication in different ways, such as auth or login. Unless you see it explicitly called like "user.authentication", you should use vector search instead.

    To search for the definition of the class "PushNotificationService": class PushNotificationService
    Use the `view_entity` tool to view all usages of the class.
    """
    if query in llm_state.ripgrep_queries:
        return DUPLICATE_RIPGREP_MESSAGE.format(question=query)
    llm_state.ripgrep_queries.add(query)
    # Future improvement: use globs/regex for both content and filename search
    # Perform content search
    content_results = perform_content_search(query, cloned_repo)
    # Combine and format results
    combined_results = format_results(query, content_results)
    # Add instructions and truncate
    final_output = add_instructions_and_truncate(combined_results, llm_state)

    return f"<ripgrep_response>\n{final_output}\n</ripgrep_response>"


@tool()
def search_for_files(
    justification: Parameter("Explain what files you are trying to find and your rationale."),  # type: ignore
    query: Parameter("The sub path to match all file paths in the repository against. All file paths that contain this sub path will be returned. You can use globs."),  # type: ignore # can be space separated
    cloned_repo: ClonedRepo,
    llm_state: LLMState,
):
    """
    Use this tool to find files in the codebase.
    Search for specific file paths in the repository, this will return all matching file paths.
    Examples:
    For searching for files, use globs:
    To find all files within a directory: <query>path/to/directory/*</query>
    To find all files within all subdirectories: <query>path/to/directory/**</query>
    To find all files that contain a subpath: <query>**/sub/path/**</query>
    To search for multiple files separate the globs/paths with spaces: <query>path/to/directory/* path/to/another/directory/***</query>
    """
    original_query = query
    # Perform filename search
    file_results = perform_filename_search(original_query, cloned_repo)
    formatted_output = ""
    if file_results.strip():
        file_results = truncate_file_results(file_results).strip("\n")
        formatted_output += f"Here are all files that contain '{query}' in the file name:\n\n<file_search_results>\n{file_results}\n</file_search_results>\n"
    else:
        # can be cleaned up later, claude likes to put multiple queries in one search with spaces in between so we enforced it
        for query in original_query.split(" "):
            # see if it tried to search for a file
            FILE_PATH_REGEX = r"(?:^|\b)((?:\.{1,2}/)?(?:[\w.-]+/)*[\w*.-]+\.[\w*-]+)(?=$|\b)"
            file_paths = re.findall(FILE_PATH_REGEX, query)
            if file_paths:
                # automatically search for the directory instead
                directory_subpath = os.path.dirname(file_paths[0])
                # we should not search the directory if there are no / as this has the chance to get all files in the codebase which would destroy the context
                if os.path.sep in directory_subpath:
                    directory_query = f"**/{directory_subpath}/***"
                    new_file_results = perform_filename_search(directory_query, cloned_repo)
                    if new_file_results.strip():
                        new_file_results = truncate_file_results(new_file_results).strip("\n")
                        # TODO: sort based on lexical similarity
                        formatted_output += f"No files were found for '{query}' However, here are all files that contain '{directory_query}' in the file name:\n\n<file_search_results>\n{new_file_results}\n</file_search_results>\n"
                else:
                    formatted_output += f"No files found for '{query}' in the codebase. If you tried to directly search for a file, instead try searching the directory you believe the file is located in. The actual file name may be different from what you assume.\n"
    return formatted_output


def perform_content_search(query: str, cloned_repo: ClonedRepo) -> str:
    if query.startswith('"') and query.endswith('"'):
        query = query[1:-1]
    if query.startswith("'") and query.endswith("'"):
        query = query[1:-1]
    joined_query = [
        "rg",
        "-n",
        "-i",
        "-C=1",
        "--heading",
        "--sort-files",
        f"'{query}'",
        cloned_repo.repo_dir,
    ]
    response = subprocess.run(
        " ".join(joined_query),
        shell=True,
        capture_output=True,
        text=True,
        cwd=cloned_repo.repo_dir,
    )
    if response.returncode == 0:
        results = cleaned_rg_output(
            root_directory=cloned_repo.repo_dir,
            sweep_config=SweepConfig(),
            output=response.stdout,
        )
        return post_filter_ripgrep_results(results)
    return ""


def perform_filename_search(query: str, cloned_repo: ClonedRepo) -> str:
    cleaned_query = query.strip("$")
    file_response = subprocess.run(
        " ".join(
            [
                "rg",
                "--files",
                "--iglob",
                f"'{cleaned_query}'",
            ]
        ),
        shell=True,
        capture_output=True,
        text=True,
        cwd=cloned_repo.repo_dir,
        # executable="rg",
    )
    if file_response.returncode == 0:
        return file_response.stdout
    return ""


def format_results(query: str, content_results: str) -> str:
    formatted_output = ""
    if content_results.strip():
        formatted_output += f"Here are ALL occurrences of '{query}' in the codebase:\n\n```\n{content_results}\n```\n"
    if not formatted_output:
        formatted_output = f"No results found for '{query}' in the codebase."
    return formatted_output


def truncate_file_results(file_results: str, threshold: int = 1000) -> str:
    lines = file_results.splitlines()
    if len(lines) > threshold:
        truncated = "\n".join(lines[:threshold])
        return f"{truncated}\n... (omitted {len(lines) - threshold} lines)"
    return file_results


def add_instructions_and_truncate(results: str, llm_state: LLMState) -> str:
    results += RIPGREP_SEARCH_RESULT_INSTRUCTIONS.format(
        request=llm_state.request,
        visited_questions="\n".join(sorted(list(llm_state.ripgrep_queries))),
    )

    MAX_RIPGREP_LINES = 1000
    result_lines = results.splitlines()
    if len(result_lines) > MAX_RIPGREP_LINES:
        truncated_results = "\n".join(result_lines[:MAX_RIPGREP_LINES])
        return f"{truncated_results}\n... (omitted {len(result_lines) - MAX_RIPGREP_LINES} lines, the massive output implies you need to be more specific in your search query)"
    return results


ACCESS_FILE_PROMPT = """Here are the contents:

<file_contents>
```
{file_contents}
```
</file_contents>

Here are other items in the same directory as {file_path}:
{files_in_directory}{entities_string}"""


@tool()
def access_file(
    justification: Parameter("Justification for why you want to access this file."),  # type: ignore
    file_path: Parameter("The path to the file you want to access. This must not be a file that was previously accessed."),  # type: ignore
    cloned_repo: ClonedRepo,
    llm_state: LLMState,
):
    """
    Displays a skeleton of a file in the codebase and add it to the currently accessed files. Only use this tool if the file has not been accessed before.
    """
    file_path = file_path.lstrip("/")
    viewed_files_key = file_path
    if viewed_files_key in llm_state.viewed_files:
        return f"\nYou have already accessed the preview for file {file_path}.\nTo view specific entities for the file, call view_entity."
    try:
        file_contents = cloned_repo.get_file_contents(file_path)
        # prevent from viewing full file multiple times. if it views the full file, it is not allowed to view it again
        llm_state.viewed_files.add(viewed_files_key)
    except FileNotFoundError as e:
        # this used to be an error, but it happens often enough that it should be a warning (the LLM will try to view a file that doesn't exist)
        logger.warning(f"Could not find file {file_path} access_file:\n{e}")
        similar_files = cloned_repo.get_similar_file_paths(file_path)
        if similar_files:
            return (
                f"ERROR\nThe file {file_path} doesn't exist in this repo, make sure the file path provided is correct.\n\nHere are some similar files in the repo:\n- "
                + "\n- ".join(similar_files)
            )
        else:
            return (
                f"ERROR\nThe file {file_path} doesn't exist in this repo, make sure the file path provided is correct."
            )
    except Exception as e:
        logger.error(f"Error calling access_file:\n{e}")
        return f"ERROR\nAn error occured while trying to access the file {file_path}. {e}"
    num_lines = len(file_contents.splitlines())

    entities_string = ""
    if num_lines > 200:
        language = file_path.split(".")[-1]
        try:
            if language not in ["py", "ts", "tsx", "js", "jsx", "java", "go"]:
                raise Exception(f"Language {language} not supported for file preview")
            get_parser(language)
        except Exception:
            logger.warning(f"Language {language} not supported for file preview, skipping")
        else:
            try:
                tree = CodeTree.from_code(file_contents, language=language)
                preview, entities, unused_entities = tree.get_preview()
                file_contents = preview
                entities_string = ""
                if unused_entities:
                    entities_string += "\n\nWARNING\nThe following entities were not found in the file:\n\n"
                    for entity in sorted(unused_entities):
                        entities_string += f"- {entity}\n"
                if entities:
                    entities_string = "\n\nHere are the collapsed entities in the file:\n\n"
                    for entity, (start_line, end_line) in sorted(entities.items(), key=lambda x: (x[1][0], x[0])):
                        entities_string += f"{entity}: {start_line} - {end_line}\n"
                    entities_string += (
                        "\nDetermine if any of the collapsed entities are relevant. If so, call the `view_entity` tool."
                    )
                    example_entity = list(entities.keys())[0]
                    entities_string += f"\n\nFor example, to view {example_entity} you would call `view_entity` with <entity>{file_path}:{example_entity}</entity>"
            except Exception as e:
                logger.error(f"Error getting preview for file {file_path}: {e}")
                entities_string = ""

    if num_lines > 8000:
        LINES_TO_SHOW = 100
        file_contents = (
            "\n".join(file_contents.splitlines()[:LINES_TO_SHOW]) + f"\n... (omitted {num_lines - LINES_TO_SHOW} lines)"
        )
        return f"Here are the first {LINES_TO_SHOW} lines of the contents:\n<file_contents>\n```\n{file_contents}\n```\n</file_contents>\nThe file {file_path} is too large to display in full. You may use the `access_file` tool to view specific sections of the file."

    try:
        file_extension = os.path.splitext(file_path)[1]
        full_directory_path = os.path.join(cloned_repo.repo_dir, os.path.dirname(file_path))
        items_in_directory = os.listdir(full_directory_path)
        files_in_directory = [f for f in items_in_directory if os.path.isfile(os.path.join(full_directory_path, f))]
        files_in_directory = sorted(files_in_directory, key=lambda x: (x.endswith(file_extension), x.lower()))
        subdirs_in_directory = [f for f in items_in_directory if os.path.isdir(os.path.join(full_directory_path, f))]
        subdirs_in_directory = sorted(subdirs_in_directory)
    except Exception as e:
        logger.error(f"Error getting directory contents for {file_path}: {e}")
        return f"ERROR\nAn error occured while trying to access the file {file_path}. {e}"

    MAX_DIRS = 20
    MAX_FILES = 50
    files_in_directory_string = "\n".join(f"- {f}" for f in files_in_directory[:MAX_FILES]) + "\n"
    if len(files_in_directory) > MAX_FILES:
        files_in_directory_string += f"... (omitted {len(files_in_directory) - MAX_FILES} files)"
    subdirs_in_directory_string = "\n".join(f"- {f}/..." for f in subdirs_in_directory[:MAX_DIRS]) + "\n"
    if len(subdirs_in_directory) > MAX_DIRS:
        subdirs_in_directory_string += f"... (omitted {len(subdirs_in_directory) - MAX_DIRS} directories)"
    return ACCESS_FILE_PROMPT.format(
        file_contents=file_contents,
        file_path=file_path,
        end=num_lines - 1,
        files_in_directory=subdirs_in_directory_string + files_in_directory_string,
        entities_string=entities_string,
    )


"""UTILITY FUNCTIONS"""


def get_function_call_message_base(**kwargs):
    """
    Use this to get the base message for a function call to let the user know what function is being called.
    """
    base_message = {
        "role": "function",
        "content": "",
        "function_call": {
            "function_name": "deciding",
            "function_parameters": "",
            "is_complete": False,
            "thinking": "",
        },
        "key": "function_call_output",
    }

    # Only update existing keys in base_message
    for key, value in kwargs.items():
        if key in base_message:
            if key == "function_call" and isinstance(value, dict):
                # For function_call, only update existing nested keys
                for fc_key, fc_value in value.items():
                    if fc_key in base_message["function_call"]:
                        base_message["function_call"][fc_key] = fc_value
            else:
                base_message[key] = value

    return Message(**base_message)


def get_imports(file_path: str, file_contents: str) -> list[tuple[int, int]]:
    """
    Gets all the line ranges of the import statements in the file.
    """
    import_ranges = []
    try:
        language = file_path.split(".")[-1]
        tree = CodeTree.from_code(file_contents, language=language)
        import_ranges = tree.get_import_line_ranges()
    except Exception as e:
        logger.error(f"Error getting imports: {e}")
        return []
    return import_ranges


def get_preview_and_entities(
    file_path: str, file_contents: str, min_lines: int = 5
) -> tuple[str, dict[str, tuple[int, int]]]:
    """
    Gets all the line ranges of the import statements in the file.
    """
    preview = ""
    entities = {}
    try:
        language = file_path.split(".")[-1]
        tree = CodeTree.from_code(file_contents, language=language)
        preview, entities, unused_entities = tree.get_preview(min_lines=min_lines)
    except Exception as e:
        logger.error(f"Error getting imports: {e}")
        return "", {}, []
    return preview, entities, unused_entities


@streamable
def search_codebase(
    question: str,
    cloned_repo: ClonedRepo,
    k=5,
    *args,
    **kwargs,
):  # -> Generator[tuple, Any, Any]:
    for message, snippets in prep_snippets.stream(cloned_repo, question, skip_analyze_agent=True, k=k, *args, **kwargs):
        yield message, snippets[:k]
    return snippets[:k]


def parse_file_names(function_call_string: str, cloned_repo: ClonedRepo) -> list[Snippet]:
    snippets = []
    try:
        for line in function_call_string.split("\n"):
            if line.startswith("<file_name>"):
                snippet_denotation = line.split("<file_name>")[1].split("</file_name>")[0]
                if ":" in snippet_denotation:
                    file_path, line_numbers = snippet_denotation.rsplit(":")
                    start, end = line_numbers.split("-")
                    file_contents = cloned_repo.get_file_contents(file_path)
                    snippets.append(
                        Snippet(
                            file_path=file_path,
                            start=int(start),
                            end=int(end),
                            content=file_contents,
                            score=1,
                        )
                    )
                else:
                    file_contents = cloned_repo.get_file_contents(file_path)
                    snippets.append(
                        Snippet(
                            file_path=file_path,
                            start=0,
                            end=len(file_contents.splitlines()),
                            content=file_contents,
                            score=1,
                        )
                    )
    except Exception as e:
        logger.error(f"Error parsing file names: {e}")
        return []
    return snippets


def construct_snippet_from_file(file_path: str, cloned_repo: ClonedRepo) -> Snippet:
    file_contents = cloned_repo.get_file_contents(file_path)
    return Snippet(
        content=file_contents,
        start=0,
        end=len(file_contents.splitlines()),
        file_path=file_path,
        score=1.0,
        type_name="source",  # TODO: classify this correctly
    )


def get_all_snippets_from_query(query: str, cloned_repo: ClonedRepo) -> list[Snippet]:
    potential_file_names_in_query: list[str] = find_filenames(query)
    mentioned_files = []
    all_existing_files: set[str] = set(cloned_repo.get_file_list())
    for potential_file_name in potential_file_names_in_query:
        if potential_file_name in all_existing_files:
            mentioned_files.append(construct_snippet_from_file(potential_file_name, cloned_repo))  # noqa: F821
        else:
            # check if it's a suffix of a unique existing file
            all_full_prefix_or_suffix_files = [
                file
                for file in all_existing_files
                if file.endswith(potential_file_name) or potential_file_name.endswith(file)
            ]
            if len(all_full_prefix_or_suffix_files) == 1:
                mentioned_files.append(construct_snippet_from_file(all_full_prefix_or_suffix_files[0], cloned_repo))
    return mentioned_files


if __name__ == "__main__":
    test_tools = [
        Tool("testing", ["abc", "def"], {}, {}, None),
        Tool("abc", ["def", "ghi"], {}, {}, None),
    ]
    #     test_response = """
    #     <function_call>
    # <ask_question_about_codebase>
    # <question>
    # Where is the vector database implementation located in the Sweep AI codebase?
    # </question>
    # </ask_question_about_codebase>
    # </function_call>
    #     """
    #     function_calls = validate_and_parse_multi_function_calls(
    #         test_response,
    #         None,
    #         test_tools
    #     )

    cloned_repo = MockClonedRepo(
        _repo_dir="/tmp/sweep-internal",
        repo_full_name="sweepai/sweep-internal",
    )

    llm_state = LLMState(
        request="",
        visited_snippets=set(),
        visited_questions=set(),
        visited_ripgrep=set(),
        ripgrep_queries=set(),
        viewed_files=set(),
    )
    # results = ripgrep("app.tsx", cloned_repo, llm_state)
    # results2 = search_for_files("testing", "sweepai/agents/*", cloned_repo, llm_state)
    file_path = "sweepai/utils/github_utils.py"
    entities = ""
    results = access_file("testing", file_path, entities, cloned_repo, llm_state)
    print(results)
