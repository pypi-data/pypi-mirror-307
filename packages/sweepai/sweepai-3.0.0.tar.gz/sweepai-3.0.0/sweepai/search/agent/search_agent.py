import re
import traceback
from copy import deepcopy
from dataclasses import dataclass

from anthropic import BadRequestError
from loguru import logger

from sweepai.config.server import DEV
from sweepai.core.entities import SNIPPET_FORMAT, Message, Snippet
from sweepai.core.github_utils import ClonedRepo
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread
from sweepai.core.llm.convert_openai_anthropic import AnthropicFunctionCall
from sweepai.dataclasses.llm_state import LLMState
from sweepai.dataclasses.use_cases import UseCase
from sweepai.core.entities import organize_snippets
from sweepai.o11y.event_logger import posthog
from sweepai.search.agent.agent_utils import (
    DUPLICATE_QUESTION_MESSAGE,
    Parameter,
    access_file,
    format_multi_function_call_results,
    get_all_snippets_from_query,
    get_function_call_message_base,
    get_imports,
    get_multi_function_calls,
    get_preview_and_entities,
    parse_file_names,
    ripgrep,
    search_codebase,
    search_for_files,
    tool,
)
from sweepai.search.agent.entity_search import (
    Definition,
    EntitiesIndex,
    Entity,
    Reference,
    parse_potential_entity_from_line,
)
from sweepai.search.agent.snippet_utils import merge_snippet_ranges
from sweepai.search.agent.summarize_directory import (
    recursively_summarize_directory,
    summarize_frameworks,
)
from sweepai.utils.diff import generate_diff
from sweepai.utils.format_utils import Prompt
from sweepai.utils.str_utils import (
    extract_object_fields_from_string,
    extract_objects_from_string,
    extract_xml_tag,
    ordered_dedup,
    pack_items_for_prompt,
    wrap_xml_tag,
)
from sweepai.utils.streamable_functions import streamable
from sweepai.utils.timer import Timer

THRESHOLD = 8000


@dataclass
class FileSearcherException(Exception):
    message: str


SEARCH_RESULT_INSTRUCTIONS_FILE_SEARCHER = """

Keep in mind you've already made these previous ripgrep queries, so you shouldn't make them again:
<previously_searched_queries>
{visited_questions}
</previously_searched_queries>"""

subsequent_search_instructions = Prompt(
    """You MUST follow the following format to reflect on your previous tool calls and determine your next steps.

Remember that here is the user's original request:
<user_request>
{{ user_request }}
</user_request>
{% if relationship_map.strip() %}
Here was your last entity relationship map:
<code_entity_relationship_map>
{{ relationship_map }}
</code_entity_relationship_map>
{% endif %}
<reflection>
List each tool call that you have just made and for each of them determine if you found the information you were looking for. For example, if you ran a vector_search to look for mocks in the codebase, determine if the vector_search output contains all the usages and implementations of the function.
a. If so, summarize the new learnings from the tool call response.
    1. For `access_file` tool calls in particular, determine whether any of the listed collapsed entities are still relevant to the user's request. If they are, access them with the `view_entity` tool.
b. If the tool call failed to find what you need, then either:
    1. Try to correct the tool call. Use broad search params or a different tool.
    2. Conclude that the information you need is not in the codebase.
</reflection>
<code_entity_relationship_map>
If you have learned something new, update the code_entity_relationship_map with the new information you have found. Otherwise, leave this empty.
</code_entity_relationship_map>
<analysis>
1. Based on the code_entity_relationship_map, explain one step at a time your current understanding of the code symbols related to the user's request.
2. Give your best answer to answer the user's request.
3. Critique your answer, and determine if there is any additional information from the codebase that you have not searched for yet that can help improve or build confidence in this answer. Only search for additional information that you have not already searched for.
</analysis>
<planning>
For each missing piece of information, determine the optimal tool to find the information you need using this strategy:
- If you know the name of the relevant entity, use `view_entity` to view the definition, dependencies, and usages.
- If you know the file name, use the `access_file` tool to access the contents of the file. If you're looking for a particular entity in this file, such as a function or a class, pass the entity name to the `entities` parameter.
- If you know the keyword that exactly matches the code you're looking for, such as the name of a code symbol, error message or user-facing copy, use the `ripgrep` tool. This is great for finding all occurrences or implementations of a code symbol.
- Otherwise, as a last resort, use the `vector_search` tool to search for relevant code blocks based on specific items. E.g. "the function that computes the user's age".
Then place all these function calls in a <function_calls></function_calls> block.

If there are no missing pieces of information, instead use the `done_file_search` tool to indicate that you are finished searching for files.
</planning>
<function_calls>
Make the function calls you have proposed in the <reflection> and <planning> blocks.
</function_calls>
"""
)

file_search_agent_system_message = Prompt("""
The assistant is Sweep, an expert software developer assigned to retrieve relevant code from a codebase to solve a user provided request regarding the repository. The request may involve writing new code, retrieving information to answer a question, or both.

In order to resolve the user request, Sweep will be given the user's request and an initial set of relevant files. Sweep may retrieve additional relevant code files from the codebase using a set of available tools to retrieve an exhaustive list of all relevant code files that will be needed to accomplish the user request.

Sweep will follow the below guidelines for aid in this task.

# Guidelines
{%- if use_case == "ticket" %}
- Sweep is generous with selecting files, prioritizing recall over precision in determining relevance. Sweep must include code files that contain relevant typing/struct/constant definitions, utility functions, or any other relevant code that is needed to best answer the user request.
{%- else %}
- Sweep is generous with selecting files, generally preferring recall over precision in determining relevance, but will give up when the tool calls stop returning new information. Sweep should retrieve code files that contain relevant definitions and utilities that is helpful for answering the user's request.
{%- endif %}
- Sweep will also include existing patterns and structures in the code base that the user should use in their solution. For example, when writing unit tests, Sweep will find a similar unit test for reference, and example usages of the function to be tested. A good place to start looking for these examples are in the same folder as the function to test.
- Sweep will use as many tools concurrently as possible to search for relevant code files. For example, Sweep may view multiple entities concurrently using the `view_entity` tool, or the `vector_search` and `ripgrep` tools to search both semantically and via keyword matching.
- Sweep will create code_entity_relationship_maps that are exhaustive, comprehensive and accurate. Only the context within the code_entity_relationship_map will be presented to the user so Sweep's code_entity_relationship_map will be as complete and informative as possible. Sweep does not need to find the location of third party dependencies.
""")

file_search_agent_instructions = """# Instructions

## Process
1. Find the primary code entity related to the user's request.
2. Understand the primary code entity's role in the codebase and how it works.
    a. Look at it's usages to understand how to invoke the code entity and it's purpose.
    b. Look at it's dependencies to understand how it works.

## Search Tool Selection Strategy

Use the following strategy to determine which tool call to make:
1. If you know the name of the relevant entity, use `view_entity` to view the definition, dependencies, and usages. This is great for understanding the code entity's purpose and how it works and should be the default tool you use.
2. If you know the file name, use the `access_file` tool to view the contents of the file.
3. If you do not know the file name but know parts of the file path, use the `search_for_files` tool to search for all possible existing files. If this tool returns nothing try expanding the search pattern before you conclude that the file doesn't exist.
4. If you know the keyword that exactly matches the code you're looking for, such as the name of the error message or user-facing copy, use the `ripgrep` tool.
5. Otherwise, as a last resort, use the `vector_search` tool to search for relevant code blocks based on concepts.

Oftentimes, it's also helpful to search for combinations, such as using both ripgrep and vector search to find the relevant code blocks.
The `search_for_files` tool is useful when files are mentioned in the user request and you need to check if they exist in the codebase.

Here's what you need to include in the Code Entity Relationship Map:

### Constructing the Code Entity Relationship Map
1. Start by identifying the code entities directly related to the user's request.
2. Identify all direct dependencies and usages of this primary entity. For example, if the primary entity is a function, use the `view_entity` tool to find all callers the function. Also, examine the function's contents to show all entities used by the function that are not in the current context.
3. If you discover a reference to an entity, such as a variable, function, class or type, not located in the current code files, use the `view_entity` tool to find the file containing the unknown entity.
4. For each code entity in the relationship map, indicate its type and relevant line ranges.

Follow this mandatory format for the Code Entity Relationship Map:

<code_entity_relationship_map>
Identify all relevant newly discovered entities and add them to the entities_to_keep block.
<entities_to_keep>
path/to/file/a.py:foo - description of the entity and it's purpose
path/to/file/b.py:bar - description of the entity and it's purpose
[list all relevant entities that are in the context, as well as file paths]
</entities_to_keep>
Identify the relationships between the entities in the following YAML format:
<entity_relationships>
[code_symbol_name]:
    explanation: An extremely detailed explanation of how this works, its purpose in the codebase, and its relevance to the user's request. If this is a function, provide a step-by-step breakdown of how it works.
    location: location
    type: function, class, variable, type etc.
    dependencies (if applicable):
        [code_symbol_name]: location
        [...repeat for all code symbols used in this code symbol's body, including third party dependencies]
    usages (if applicable):
        [code_symbol_name]: location
        [...repeat for all code symbols used by this code symbol]
    related_symbols (optional):
        [code_symbol_name]: location
        [...repeat for all code symbols that are similar or related to this code symbol]
[...repeat for all code symbols]

Locations are either of the format path/to/file.py:a-b or a question mark.
</entity_relationships>
<missing_information>
List all missing information that you will need to retrieve, including:
- The definitions of symbols
- The dependencies of a certain symbol
- The usages of a certain symbol, especially for testing
</missing_information>
Example:
<example>
<entities_to_keep>
data_processing.py:process_data - Processes raw data, applies transformations, and prepares it for analysis and reporting
data_validation.py:validate_input - Validates input data to ensure it meets required format and quality standards
constants.py:DATA_THRESHOLD - Defines a threshold value used in data processing operations
formatting_utils.py:format_data - Formats processed data into a specific structure or output format
reporting.py:generate_report - Creates a comprehensive report based on processed data, including summaries and analysis results
logging_config.py:setup_logging - Configures the logging system for the application, setting up log levels and output formats
reporting.py:DataAnalyzer - A class that performs various data analysis tasks on processed data
error_handling.py:handle_error - Manages error handling, including logging and potential recovery procedures
</entities_to_keep>
<entity_relationships>
process_data:
    explanation: The function begins by processing raw data through a series of transformations and calculations. Initially, it validates the input data using the validate_input function to ensure that the data meets the necessary criteria for further processing. Once the input is validated, the function applies a threshold defined by the constant DATA_THRESHOLD. This threshold is used to filter the data, ensuring that only relevant data points are considered for subsequent operations.
    location: src/data_processing.py:64-131
    type: function
    dependencies:
        validate_input: src/data_processing.py:50-95
        DATA_THRESHOLD: src/data_processing.py:23-36
        UnvalidatedData: ? # unknown input type
        np.array: numpy # third party
        pandas.DataFrame: pandas # third party
    usages:
        generate_report: src/reporting.py:112-140
        DataAnalyzer: ? # caller with unknown location
    related_symbols:
        error_handling.py: Contains similar error handling structure
        data_validation.py: Uses similar input validation techniques

validate_input:
    explanation: This function checks the integrity and format of input data before processing. It likely performs type checking, range validation, and possibly checks for missing or inconsistent values. The function helps ensure that only valid data is processed, preventing errors in downstream operations.
    location: src/data_validation.py:50-95
    type: function
    description: Validates input data to ensure it meets required format and quality standards.

DATA_THRESHOLD:
    explanation: This constant defines a threshold value used in data processing. It may represent a cutoff point for filtering data, a minimum or maximum acceptable value, or a reference point for normalization.
    location: src/constants.py:23-36
    type: constant
    description: Defines a threshold value used in data processing operations.

format_data:
    explanation: This utility function is responsible for formatting processed data into a specific structure or format. It likely handles tasks such as rounding numbers, converting data types, or organizing data into a particular layout for output or further processing.
    location: src/formatting_utils.py
    type: function
    description: Formats processed data into a specific structure or output format.
</entity_relationships>
<missing_information>
The location and definition of the DataAnalyzer class.
All other usages of process_data.
</missing_information>
</example>

In this example, further `view_entity` calls would be needed if any types or locations were unknown. Under relevant_symbols, include files with relevant example patterns or structures for the user's solution, typically found in the same directory as the primary code entity using the search_for_files tool.
Note that all entities are relevant to better understanding the primary code entity, and relevant line numbers are included.
</code_entity_relationship_map>

Your task is incomplete until you've fully built this Code Entity Relationship Map, including all relevant entities and definitions related to the user's request. You do not need to find the location of third party dependencies.

# Tools

## Tool Format
In this environment you have access to tools that can help you find the relevant code files needed to answer the user's request. You may make multiple tool calls at once.

You MUST call tools like this:
<function_calls>
<function_call>
<tool_name>
<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>
...
</tool_name>
</function_call>
[other function calls]
</function_calls>

"""

file_search_agent_user_message = """# Context

You will be searching for files in the {repo} repository.

Here is the initial context provided for you to work off of.

<initial_context>
{existing_context}

<summary>
{summary}
</summary>
</initial_context>

Here is a summary of some of the key directories in the codebase:

<directory_tree>
{directory_tree}
</directory_tree>

<directory_summaries>
{directory_summaries}
</directory_summaries>

<repository_summary>
{repo_summary}
</repository_summary>

{instructions}

Here is the user's current request that you must satisfy:

<user_request>
{user_request}
</user_request>

# Format

Respond in the following format:

{user_request_analysis}

<context_analysis>
1. Analyze the existing context and list all content relevant to the subrequests in extreme detail and mention all relevant code symbols.
2. Create a code_entity_relationship_map for the existing context.
</context_analysis>

<stack_analysis>
Analyze the <summary> and <stack> blocks to determine if there are any important pieces of information about the codebase's conventions and structures that are relevant to the user's request. Based on this, infer any naming conventions for the codebase if possible.
</stack_analysis>

<planning>
### Checking Existing Context
List each subrequest and determine if the information is in the existing context:
1. **[replace this with the information to search for]**:
    - Look carefully to determine if the information is in the existing context.
    - For example, if you're trying to find an example of mocks in the codebase, look at the existing context to see if it contains any examples of mocks.
    - If so, this subrequest is complete.
    - If not, give your best answer based on the initial context.
[list for each subrequest]

### Plan Tool Call
List each incomplete subrequest and use the strategy to determine the optimal tool call:
1. **[replace this with the information to search for]**: (follow this strategy)
    - If you know the name of the relevant entity, use `view_entity` to view the definition, dependencies, and usages. This is great for understanding the code entity's purpose and how it works and should be the default tool you use.
    - If you know the file name, use the `access_file` tool to view the contents of the file.
    - If you do not know the file name but know parts of the file path, use the `search_for_files` tool to search for all possible existing files. If this tool returns nothing try expanding the search pattern before you conclude that the file doesn't exist.
    - If you know the keyword that exactly matches the code you're looking for, such as the name of the error message or user-facing copy, use the `ripgrep` tool.
    - Otherwise, as a last resort, use the `vector_search` tool to search for relevant code blocks based on concepts.
[list for each subrequest]

Please carefully review all files provided in the <initial_context> section. These files contain important information needed to complete the task. Always refer back to this context before assuming information is missing.

If the existing context is already enough to resolve the user's request, call `done_file_search` right away.
</planning>

<function_calls>
Then, make EACH of the proposed tool calls under <planned_tool_calls> here. You can make multiple tool calls at once:
<function_call>
[...]
</function_call>
<function_call>
[...]
</function_call>
[repeat for all function calls]
</function_calls>"""

first_message_user_instructions = """<user_request_analysis>
Analyse the user's request and summarize the information needed to resolve the user's request.
- For example, what is the aim of the user's request? Are they looking for information? Are they asking you to write new code?
- If they are looking for information, does the current context contain all the information needed to resolve the user's request?
- If they are asking you to write new code, what information do you need to write the code?

Break down the user's request into the smallest subrequests:
1. *[replace with the first subrequest]*
2. *[replace with the second subrequest]*
...
For example, if the user is asking for a unit test, one subrequest would be to check if there is already an existing test file.

Keep in mind that the information within the user's request may not be fully accurate and you may need to make some assumptions.
</user_request_analysis>"""

follow_up_user_instructions = """<user_request_analysis>
First, summarize the thread history to determine what the user originally asked for, what has been done so far, and what the user needs next.

Analyse the user's request and summarize the information needed to resolve the user's request.
- For example, what is the aim of the user's request? Are they looking for information? Are they asking you to write new code?
- If they are looking for information, does the current context contain all the information needed to resolve the user's request?
- If they are asking you to write new code, what information do you need to write the code?

Break down the user's request into the smallest subrequests:
1. *[replace with the first subrequest]*
2. *[replace with the second subrequest]*
...
For example, if the user is asking for a unit test, one subrequest would be to check if there is already an existing test file.

Keep in mind that the information within the user's request may not be fully accurate and you may need to make some assumptions.
</user_request_analysis>"""

# rework these
example_tool_calls_file_searcher = """Here are illustrative examples of how to use the tools:

<examples>
<example>
<user_message>
Write unit tests for compute_black_scholes in src/lib/financial/black_scholes.py
</user_message>

<function_calls>
<function_call>
<view_entity>
<justification>
We need to find the definition of compute_black_scholes in src/lib/financial/black_scholes.py, as well as it's dependencies and usages.
</justification>
<entity>
src/lib/financial/black_scholes.py:compute_black_scholes
</entity>
</view_entity>
</function_call>
<function_call>
<vector_search>
<justification>
We need to check for existing unit tests for compute_black_scholes. All unit tests appear to be in tests directory and are prefixed with test_.
</justification>
<question>
unit test compute_black_scholes
</question>
<globs>tests/**/test_black_scholes.py</globs>
</vector_search>
</function_call>
</function_calls>

This example shows how to find the definition, and all dependencies and usages of a code symbol. It also shows how to find existing unit tests for a function.
</example>

<example>
<user_message>
Replace all usages of truncate from strUtils.ts to use lodash instead.
</user_message>

<function_calls>
<function_call>
<view_entity>
<justification>
We need to find all usages of truncate to replace them with lodash.
</justification>
<entity>
strUtils.ts:truncate
</entity>
</view_entity>
</function_call>
</function_calls>

This examples shows how to find all usages of a code symbol in the codebase.
</example>

<example>
<user_message>
Add input validation to the user registration handler using the go-playground/validator package.
</user_message>

<function_calls>
<function_call>
<vector_search>
<question>
user registration handler Go
</question>
<globs>cmd/**/*.go internal/handlers/**/*.go pkg/api/**/*.go</globs>
</vector_search>
</function_call>
<function_call>
<ripgrep>
<justification>
We need to find where user data is currently being processed in the registration handler.
</justification>
<query>
func.*Register|json.Unmarshal.*User
</query>
</ripgrep>
</function_call>
<function_call>
<search_for_files>
<justification>
We need to check if go-playground/validator is already set up in the project.
</justification>
<query>
go.mod
</query>
</search_for_files>
</function_call>
<function_call>
<search_for_files>
<justification>
We need to check if go-playground/validator is already set up in the project.
</justification>
<query>
**/*validator*.go
</query>
</search_for_files>
</function_call>
</function_calls>

This example shows how to locate the user registration handler in a Go project, identify current data processing patterns, and check for existing validator setup, all in one set of function calls.
</example>

<example>
<user_message>
Implement JWT refresh token functionality in the login process.
</user_message>

<function_calls>
<function_call>
<vector_search>
<question>
login process JWT implementation
</question>
<globs>src/auth/**/*.ts src/controllers/**/*.ts</globs>
</vector_search>
</function_call>
<function_call>
<ripgrep>
<justification>
We need to find where the JWT is currently being generated and sent to the client.
</justification>
<query>
jwt.sign|generateToken
</query>
</ripgrep>
</function_call>
<function_call>
<vector_search>
<question>
token storage user login session
</question>
<globs>src/models/**/*.ts src/services/**/*.ts</globs>
</vector_search>
</function_call>
</function_calls>

This example demonstrates how to find the current JWT implementation in the login process, locate token generation code, and identify potential places for storing refresh tokens, all in one set of function calls.
</example>

We should make as many relevant function calls together as possible to gather maximal information efficiently. Always tailor your search queries to the specific user request and context of the codebase.
</examples>

The above are illustrative examples. Adapt your search queries and tool usage to the specific user request and codebase context."""

existing_snippet_format = """<accessed_code_block index="{index}">
<source>{file_path}</source>
<accessed_code_block_content>
{source}
</accessed_code_block_content>
</accessed_code_block>"""

existing_file_format = """<accessed_file index="{index}">
<source>{file_path}</source>
<accessed_file_content>
{source}
</accessed_file_content>
</accessed_file>"""

USER_REQUEST_PLACEHOLDER = "The user's request has been deduplicated for brevity. Refer to the bottommost user request."


def get_parent_scope(entity: Entity) -> str:
    parent = entity.parent
    while parent:
        if parent.entity_type in ("function", "method", "class"):
            return parent
        parent = parent.parent
    return None


@tool()
def view_entity(
    justification: Parameter("Justification for why you want to view this entity."),  # type: ignore
    entity: Parameter("The entity to view, in the format file_path:symbol. This should be a string that uniquely identifies the entity in the codebase."),  # type: ignore
    llm_state: LLMState,
):
    """
    View the definition and all dependencies and usages of a code symbol in the codebase.

    This must be in the format file_path:symbol. If file path is not provided the search will be for all occurrences of the symbol in the codebase.

    Examples:
    <examples>
    1. To find the definition and usages of the function `compute_total` in the file `calculations.py`:
        Use the entity <entity>calculations.py:compute_total</entity>
    2. To find all usages of the function `compute_total` in the codebase:
        <entity>compute_total</entity>
    </examples>
    """
    entities_index = llm_state.entities_index
    if ":" not in entity:
        file_path = ""
        symbol = entity
    else:
        # Some languages (e.g., C++) use '::' for namespacing or scope resolution
        # This handles cases where the entity might be in the format 'namespace::symbol'
        file_path, symbol = parse_potential_entity_from_line(entity)
    results = ""
    entities_data = entities_index.get_entities_data(symbol, file_path)
    definitions = entities_data["definitions"]
    if definitions:
        if len(definitions) > 1:
            results += f"We found {len(definitions)} definitions for {symbol} in the codebase. Here is the best match:\n"
        entity = definitions[0]
        results += f"<entity>{entity.file_path}:{entity.name}</entity>\n"
        results += f"Here is the definition of {symbol}:\n"
        results += wrap_xml_tag(entity.contents, "definition") + "\n"
    usages = entities_data["usages"]
    if usages:
        results += f"\n<usages>\n"
        results += f"We found {len(usages)} usages of {symbol} in the codebase:\n"
        k = 10
        for usage in usages[:k]:
            results += f"<usage>\n"
            results += f"{usage.file_denotation}\n"
            parent_scope = get_parent_scope(usage) or usage.parent
            parent_contents = parent_scope.contents if parent_scope else ""
            header = ""
            for line in parent_contents.split("\n"):
                if line.strip().startswith("@"):
                    header += line + "\n"
                    continue
                header += line
                break
            results += f"{header}\n    ...\n\n"
            results += f"{usage.contents}\n"
            results += f"</usage>\n"
        if len(usages) > k:
            results += (
                f"... {len(usages) - k} other usages of {symbol} hidden for brevity.\n"
            )
        results += f"</usages>\n"
    defined_dependencies = [
        dep
        for dep in entities_data["dependencies"]
        if dep.origin_type == "defined" and dep.referenced_entity.scope == "global"
    ]
    defined_dependencies = ordered_dedup(defined_dependencies, key=lambda dep: dep.name)
    if defined_dependencies:
        results += f"\n<defined_dependencies>\n"
        results += f"We found {len(defined_dependencies)} dependencies of {symbol} defined in this file:\n"
        for dependency in defined_dependencies:
            results += f"<defined_dependency>\n"
            results += (
                wrap_xml_tag(
                    f"{dependency.name} in {dependency.file_denotation}", "entity"
                )
                + "\n"
            )
            results += wrap_xml_tag(dependency.contents.strip(), "contents") + "\n"
            results += f"</defined_dependency>\n"
        results += f"</defined_dependencies>\n"
    dependencies: list[Reference] = [
        dep
        for dep in entities_data["dependencies"]
        if dep.origin_type not in ("builtin", "defined")
    ]
    dependencies = ordered_dedup(dependencies, key=lambda dep: dep.name)
    if dependencies:
        results += f"\n<dependencies>\n"
        results += (
            f"We found {len(dependencies)} dependencies of {symbol} in the codebase:\n"
        )
        for dependency in dependencies:
            results += f"<dependency>\n"
            results += (
                wrap_xml_tag(
                    f"{dependency.name} in {dependency.file_denotation}", "entity"
                )
                + "\n"
            )
            results += wrap_xml_tag(dependency.contents.strip(), "contents") + "\n"
            if dependency.resolved_entity:
                results += (
                    wrap_xml_tag(dependency.resolved_entity.full_reference, "origin")
                    + "\n"
                )
            results += f"</dependency>\n"
        results += f"</dependencies>\n"
    if not definitions:
        if usages:
            results = (
                f"No definition of {symbol} were found in the codebase. However, there are {len(usages)} usages of {symbol} in the codebase. This code symbol is likely to be either a third-party library or is auto-generated.\n\n"
                + results
            )
        else:
            results = f"No definitions or references of {symbol} were found in the codebase. This code symbol is likely to be either a third-party library or is auto-generated."
            # TODO: use ripgrep here instead
    return results


@tool()
@streamable
def vector_search(
    question: Parameter("A question with specific keywords to search the codebase for relevant code blocks."),  # type: ignore
    globs: Parameter("The glob patterns to search for the code blocks. Leave as */* to match all files. Use this to isolate the search to a specific directory or file type. * matches anything, including directories. You may use multiple globs separated by spaces."),  # type: ignore
    cloned_repo: ClonedRepo,
    llm_state: LLMState,
):
    """
    Performs a semantic search on the codebase to find relevant code blocks.

    Use this when you don't know the exact name of the code symbol you are looking for, but you have a general idea of the concept you are searching for. Format your question as a set of keywords and avoid unnecessary words that might reduce the accuracy of the search results. Ensure the globs are from the root of the codebase.

    Examples:
    <examples>
    1. To find the function in the frontend that computes the user's age:
        Use the question "compute user age" with globs set to:
        <globs>src/frontend/services/booking/*.tsx src/frontend/services/booking/*.ts</globs>
        if you know the function is in the booking service and is a ts or tsx file.
    2. To find the test that checks if push notifications are sent in the backend:
        Use the question "test push notifications sent" with globs set to:
        <globs>tests/backend/*.py</globs>
        if you know the test is in the tests directory and is a python file.
    </examples>
    """
    globs = globs.split(" ")
    logger.info(globs)
    previously_asked_question = deepcopy(llm_state.visited_questions)
    if not question.strip():
        yield "Question cannot be empty. Please provide a detailed, specific natural language search question to search the codebase for relevant code blocks."
    if question in llm_state.visited_questions:
        yield DUPLICATE_QUESTION_MESSAGE.format(question=question)
    llm_state.visited_questions.add(question)
    snippets: list[str] = []
    message: str
    retrieved_snippets: list[Snippet]
    for message, retrieved_snippets in search_codebase.stream(
        question=question,
        cloned_repo=cloned_repo,
        globs=globs,
    ):
        yield message
    prev_visited_snippets = deepcopy(llm_state.visited_snippets)
    index = 1
    for snippet in retrieved_snippets[::-1]:
        if snippet.denotation not in llm_state.visited_snippets:
            expand_size = 100
            snippets.append(
                SNIPPET_FORMAT.format(
                    denotation=snippet.expand(expand_size).denotation,
                    contents=snippet.expand(expand_size).get_snippet(add_lines=True),
                    index=index,
                )
            )
            index += 1
            llm_state.visited_snippets.add(snippet.denotation)
        else:
            snippets.append(
                f"Code block already retrieved previously: {snippet.denotation}"
            )
    snippets_string = "\n\n".join(snippets)
    snippets_string = f"<code_blocks>\n{snippets_string}\n</code_blocks>"
    snippets_string += (
        f'\n\nYour last search question was "{question}". Here is a list of all the files retrieved in this search question:\n'
        + "\n".join([f"- {snippet.denotation}" for snippet in retrieved_snippets])
    )
    if prev_visited_snippets:
        snippets_string += (
            "\n\nHere is a list of all the files retrieved previously:\n"
            + "\n".join(
                [f"- {snippet}" for snippet in sorted(list(prev_visited_snippets))]
            )
        )
    snippets_string += f'\n\nThe above are the code blocks that are found in decreasing order of relevance to the search question "{question}".'
    if previously_asked_question:
        snippets_string += (
            "\n\nYou have already asked the following questions so do not ask them again:\n"
            + "\n".join([f"- {question}" for question in previously_asked_question])
        )
    warning_messages = ""
    yield snippets_string + SEARCH_RESULT_INSTRUCTIONS_FILE_SEARCHER.format(
        request=llm_state.request.strip("\n"),
        visited_questions="\n".join(sorted(list(llm_state.visited_questions))),
    ) + warning_messages


def add_snippet_to_context(
    file_names: list[str], cloned_repo: ClonedRepo, relevant_files: list[Snippet]
) -> tuple[list[str], list[str]]:
    """
    Adds string of the form: file_path:start_line-end_line to relevant_files
    If a snippet fails to get added, the filename is returned in bad_files
    Snippets that are too large will have their filename returned in large_files
    """
    bad_files: list[str] = []
    large_files: list[str] = []
    existing_files = set([snippet.file_path for snippet in relevant_files])
    for file_to_add in file_names:
        file_range: list[int] = []
        file_name = file_to_add
        if ":" in file_to_add:
            # some file names can have : in their file name example: path/to/object/:objectid.ext
            file_name, line_range = file_to_add.rsplit(":", 1)
            try:  # attempt to parse the line range if not add the whole thing and log it
                if "-" in line_range:
                    file_range = [int(num) for num in line_range.split("-")]
                else:
                    file_range = [int(line_range), int(line_range)]
            except Exception:
                logger.error(
                    f"Error parsing line range for file {file_to_add} with range {line_range}. Adding the whole file to context."
                )
                file_range = []

        # make sure the file exists in the cloned_repo
        file_contents = ""
        try:
            file_contents = cloned_repo.get_file_contents(file_name)
        except FileNotFoundError:
            bad_files.append(file_name)
            continue

        if file_contents:
            file_lines = file_contents.splitlines()
        else:
            file_lines = [""]
        file_length = len(file_lines)
        # if file name is already in context than make sure ranges dont overlap and if they do merge them
        if file_name in existing_files:
            if file_range:
                # all snippet ranges
                all_ranges = []
                snippet_indexes = []
                for i, snippet in enumerate(relevant_files):
                    if snippet.file_path == file_name:
                        all_ranges.append((snippet.start, snippet.end))
                        snippet_indexes.append(i)
                all_ranges.append(file_range)
                # check if the new range overlaps with any of the existing ranges and merge them
                new_ranges = merge_snippet_ranges(all_ranges, context_lines=20)
                # remove and recreate the snippets
                for i in snippet_indexes[::-1]:
                    relevant_files.pop(i)
                for start, end in new_ranges:
                    relevant_files.append(
                        Snippet(
                            content=file_contents,
                            start=start,
                            end=end,
                            file_path=file_name,
                            score=1,
                        )
                    )
            # adding whole file so we just overwrite the entire file
            else:
                snippet_indexes = []
                first_occurence = True
                for i, snippet in enumerate(relevant_files):
                    if snippet.file_path == file_name:
                        if first_occurence:
                            snippet.start = 1
                            snippet.end = file_length
                            first_occurence = False
                        else:
                            snippet_indexes.append(i)
                # now that the snippet is the whole file there is no need for the other snippets
                # iterate backwards through relevant files and pop the indexes
                for i in snippet_indexes[::-1]:
                    relevant_files.pop(i)
        elif file_length > THRESHOLD:
            large_files.append(file_name)
        else:  # otherwise we add the snippet
            start = 1
            end = file_length
            if file_range:
                start, end = file_range
            relevant_files.append(
                Snippet(
                    content=file_contents,
                    start=start,
                    end=end,
                    file_path=file_name,
                    score=1,
                )
            )
    return bad_files, large_files


@tool()
def update_user(
    issue: Parameter("Briefly and concisely explain the issue you are facing in resolving some aspect of the user's request. Assume the user will be reading this portion of your response."),  # type: ignore
    justification: Parameter("Explain in detail what steps you have taken in order to try and resolve this aspect of the user's request and why it has been unsuccessful so far. Assume the user will be reading this portion of your response."),  # type: ignore
    update: Parameter("Inform the user of what new assumptions you will have to make in order to overcome this issue and attempt to resolve the rest of the user's request to the best of your ability. Assume the user will be reading this portion of your response."),  # type: ignore
):
    """
    If there is an aspect of the user request that you are unable to resolve, you must use this tool to let the user know what it is that you are not able to resolve and why.
    Let the user know what you have found and what you have not been able to find. Let the user know what new assumptions you have to make in order to resolve the rest of the user's request. When calling this tool, assume that the user will be reading your response and as such adopt an appropriate tone and level of detail in your response.
    You should not call this tool until you are absolutely sure that you are unable to resolve some aspect of the user request. This means that you have searched at least twice with the `vector_search` tool and the `ripgrep` tool.


    Here is an example use case for this `update_user` tool:
    Example user request: "Please write a unit test covering the case when I click the 'View Tests' button in the /src/components/Tests.js file."
    Example usage:
    <update_user>
    <issue>
    I am unable to find the `View Tests` button inside the file /src/components/Tests.js file.
    </issue>
    <justification>
    I have examined the /src/components/Tests.js file in its entirety and have not been able to identify a `View Tests` button.
    I have also searched the code base to find other possible relevant places where this `View Tests` button could be located but I have only been able to find it in completely unrelated files such as /src/components/Cars/Brands.js.
    However, I have found a `View Tests Preview` checkbox in the /src/components/Tests.js file.
    </justification>
    <update>
    Instead of writing a unit test for the `View Tests` button, I will instead write a unit test for the `View Tests Preview` checkbox since that is the closest match I could find and there is currently no unit test for the `View Tests Preview` checkbox.
    I believe this is the best way to proceed given the information I have found.
    </update>
    </update_user>
    """

    return "SUCCESSFULLY UPDATED USER!"


def parse_snippets_from_code_entity_relationship_map(
    code_entity_relationship_map: str,
    cloned_repo: ClonedRepo,
    entities_index: EntitiesIndex,
) -> list[str]:
    """
    Parses all snippets to add to context from the code_entity_relationship_map created by Sweep
    """
    snippets_to_add: list[str] = []
    if not code_entity_relationship_map:
        return []
    entities_to_keep = extract_xml_tag(code_entity_relationship_map, "entities_to_keep")
    if not entities_to_keep:
        return []
    for line in entities_to_keep.splitlines():
        try:
            if " - " in line:
                line, _justification = line.split(" - ")
            if ":" not in line:
                file_contents = cloned_repo.get_file_contents(line)
                snippets_to_add.append(f"{line}:1-{len(file_contents.splitlines())}")
                continue
            file_path, reference = line.rsplit(":", 1)
            if "-" in reference:
                snippets_to_add.append(line)
            else:
                if file_path not in entities_index.entities_mapping:
                    continue
                entity = entities_index.entities_mapping[file_path].definitions.get(
                    reference
                )
                if entity:
                    snippets_to_add.append(
                        f"{file_path}:{entity.start_line}-{entity.end_line}"
                    )
        except Exception as e:
            logger.error(
                f"Error parsing snippet from code_entity_relationship_map: {e}"
            )
            # Assuming posthog is imported and configured
            posthog.capture(
                f"parse_snippets_from_code_entity_relationship_map",
                "parse_snippets_from_code_entity_relationship_map error",
                properties={
                    "error": str(e),
                    "traceback": str(traceback.format_exc()),
                    "code_entity_relationship_map": code_entity_relationship_map,
                },
            )
    return snippets_to_add


@tool()
def done_file_search(
    reason: Parameter("Justification for why you are calling this tool and why you have found all relevant code files."),  # type: ignore
    code_entity_relationship_map: Parameter("Include the final Code Entity Relationship Map you generated. Include as much detail as possible. The correctness and completeness of this Code Entity Relationship Map is crucial as it will be used as proof for your answer. It is mandatory for you to include the line numbers inside the Code Entity Relationship Map."),  # type: ignore
    existing_patterns: Parameter("When applicable and if possible, identify a similar pre-existing feature in the codebase. Then, list precisely how that feature is implemented. Finally, explain how we can implement the requested feature similarly. If this field is not applicable simply leave it blank.", optional=True),  # type: ignore
    relevant_files: list[Snippet],
    cloned_repo: ClonedRepo,
    llm_state: LLMState,
    justification: str = "",  # breaks without this line
):
    """
    Once you are confident you have found and added ALL relevant files to the context you may call this tool to indicate that you are finished.
    Before calling this tool, make sure you have been able to resolve all aspects of the user request to the best of your ability. If this is not the case, you must use the `update_user` tool to inform the user of what you have found and what you have not been able to find.
    """
    snippets_to_add: list[str] = parse_snippets_from_code_entity_relationship_map(
        code_entity_relationship_map, cloned_repo, llm_state.entities_index
    )
    # parse out snippets from the code_entity_relationship_map
    _bad_files, _large_files = add_snippet_to_context(
        snippets_to_add, cloned_repo, relevant_files
    )

    # now we review all snippets added to context and make some tweaks based on the following heuristics
    # for files under MIN_FILE_LENGTH we will add the entire file to context instead
    # always include the imports for the files
    # if there are snippets that are only a few lines long expand them to include the entire function or class, or if not applicable just expand +- CONTEXT_LENGTH lines above and below
    MIN_FILE_LENGTH = 1000
    _CONTEXT_LENGTH = 5

    files_to_update: list[str] = []

    # check for any snippets under min length
    for snippet in relevant_files:
        file_contents = snippet.content
        file_lines = file_contents.splitlines()
        file_length = len(file_lines)

        # For files under MIN_FILE_LENGTH, add the entire file to context
        if file_length <= MIN_FILE_LENGTH:
            if snippet.file_path not in files_to_update:
                files_to_update.append(f"{snippet.file_path}")
    # Update snippets with new ranges
    if files_to_update:
        add_snippet_to_context(files_to_update, cloned_repo, relevant_files)

    # TODO this section might have a bug

    # loop through our current snippets to find any snippets that encapsulate an entire entity
    # then find if there are other places in the file where that entity is mentioned and create snippets out of those also
    entity_callers_to_add: list[str] = []
    for snippet in relevant_files:
        mentioned_entities: list[str] = []
        file_contents = snippet.content
        file_lines = file_contents.splitlines()
        file_length = len(file_lines)
        if snippet.file_path not in files_to_update:
            # get the context around the snippet
            # this is a bit wasteful since we call it again in the below for loop but overall is not too big of an issue
            # logic is easier to write this way
            _preview, entities, unused_entities = get_preview_and_entities(
                snippet.file_path, snippet.content, min_lines=0
            )
            for entity_name, line_range in entities.items():
                # give a bit of wiggle room for the entity start and end
                entity_start = line_range[0] - 1
                entity_end = line_range[1] + 1
                if (snippet.start <= entity_end and snippet.start >= entity_start) or (
                    snippet.end >= entity_start and snippet.end <= entity_end
                ):
                    mentioned_entities.append(entity_name)
        # if we have mentioned entities in this file we should search for the lines they appear on and add those to context
        if mentioned_entities:
            # get all lines where the entities are mentioned
            for index, line in enumerate(file_lines):
                if any(entity in line for entity in mentioned_entities):
                    # add the line to context
                    # once again this is a bit wasteful but easier to write
                    # optimal we should only add the lines that are not already in context but can improve later
                    # add +/- context lines)
                    entity_callers_to_add.append(
                        f"{snippet.file_path}:{index + 1}-{index + 1}"
                    )
    if entity_callers_to_add:
        add_snippet_to_context(entity_callers_to_add, cloned_repo, relevant_files)

    entities_to_add: list[str] = []
    # expand all snippets to include the entire entity
    for snippet in relevant_files:
        mentioned_entities: list[str] = []
        if snippet.file_path not in files_to_update:
            file_contents = snippet.content
            file_lines = file_contents.splitlines()
            file_length = len(file_lines)
            # get the context around the snippet
            _preview, entities, unused_entities = get_preview_and_entities(
                snippet.file_path, snippet.content, min_lines=0
            )
            for entity_name, line_range in entities.items():
                entity_start = line_range[0]
                entity_end = line_range[1]
                # this logic can be expanded to include +1 and -1 entity by adding or subtracting some amount to the snippet start and end
                if (snippet.start <= entity_end and snippet.start >= entity_start) or (
                    snippet.end >= entity_start and snippet.end <= entity_end
                ):
                    entities_to_add.append(
                        f"{snippet.file_path}:{line_range[0]}-{line_range[1]}"
                    )
    if entities_to_add:
        add_snippet_to_context(entities_to_add, cloned_repo, relevant_files)

    more_files_to_update: list[str] = []
    # now for remaining snippets make sure to always include the import
    for snippet in relevant_files:
        if snippet.file_path not in files_to_update:
            # check if the imports are included or not
            import_line_ranges = get_imports(snippet.file_path, snippet.content)
            if import_line_ranges:
                merged_import_ranges = merge_snippet_ranges(
                    import_line_ranges, context_lines=5
                )
                # now for each range add those snippets to the context
                for start, end in merged_import_ranges:
                    more_files_to_update.append(f"{snippet.file_path}:{start}-{end}")
            else:
                # failed to get imports or imports didn't exist
                logger.warning(f"Failed to get imports for file {snippet.file_path}")

    # Update snippets with new ranges
    if more_files_to_update:
        add_snippet_to_context(more_files_to_update, cloned_repo, relevant_files)

    return "DONE"


file_searcher_tools = [
    view_entity,
    search_for_files,
    access_file,
    ripgrep,
    vector_search,
    done_file_search,
]

file_searcher_tools_available = """# Available Tools

Here is a list of all the tools you have access to and how you can invoke them:

""" + "\n\n".join(
    tool.get_xml() for tool in file_searcher_tools
)


def file_searcher_context_cleanup(thread: Thread):
    """
    Clean up context for file searcher. Called near the beginning of the file_searcher function.
    """
    messages = thread.messages
    for message in messages:
        # turn code_change blocks to diffs
        # fetch all code_change blocks in order
        code_changes, failed = extract_objects_from_string(
            message.content, "code_change", ["file_path", "original_code", "new_code"]
        )
        if not failed:
            for code_change in code_changes:
                # build diff
                diff = generate_diff(
                    code_change["original_code"], code_change["new_code"]
                )
                # replace code_change block with diff
                start_index = message.content.index("<code_change>")
                end_index = message.content.index("</code_change>")
                # replace code_change block with diff
                message.content = (
                    message.content[:start_index]
                    + f"\n{diff}\n"
                    + message.content[end_index + len("</code_change>") :]
                )

        # remove all snippets from context, this are most likely results from vector searches, plus all relevant snippets will already be in the last user message
        # this will fetch all snippets in order in the message
        snippets, failed = extract_objects_from_string(
            message.content, "snippet", ["file_name", "source"]
        )
        if not failed:
            for snippet in snippets:
                # remove snippet from context
                snippet_file_name = snippet["file_name"]

                # replace the entire snippet with a string
                start_index = message.content.index("<snippet>")
                end_index = message.content.index("</snippet>")
                message.content = (
                    message.content[:start_index]
                    + f"\nFetched snippet {snippet_file_name} (content not currently shown)\n"
                    + message.content[end_index + len("</snippet>") :]
                )
        # remove all ripgrep results from context if they are over a certain length
        RIPGREP_CONTEXT_THRESHOLD = 2500
        ripgrep_results, failed = extract_objects_from_string(
            message.content, "ripgrep_response", []
        )
        if not failed:
            for ripgrep_result in ripgrep_results:
                # remove ripgrep result from context
                ripgrep_contents = ripgrep_result["content"]
                if len(ripgrep_contents) > RIPGREP_CONTEXT_THRESHOLD:
                    start_index = message.content.index("<ripgrep_response>")
                    end_index = message.content.index("</ripgrep_response>")
                    message.content = (
                        message.content[:start_index]
                        + f"\n(Ripgrep result is too large to display)\n"
                        + message.content[end_index + len("</ripgrep_response>") :]
                    )
        view_file_contents, failed = extract_objects_from_string(
            message.content, "file_contents", []
        )
        if not failed:
            for view_file_content in view_file_contents:
                file_contents = view_file_content["content"]
                # remove view_file result from context
                start_index = message.content.index("<file_contents>")
                end_index = message.content.index("</file_contents>")
                message.content = (
                    message.content[:start_index]
                    + f"\nFile contents:\n{file_contents[:100]}... (rest of content not currently shown)\n"
                    + message.content[end_index + len("</file_contents>") :]
                )
    # now merge consecutive messages with key function_call together and dedupe them
    new_messages = []
    merged_message = None
    for message in messages:
        if message.key == "function_call":
            if merged_message is None:
                merged_message = deepcopy(message)
            else:
                # only add if not already in message contents no need to double add
                if message.content.strip() not in merged_message.content:
                    merged_message.content += f"\n{message.content}"
        else:
            if merged_message is not None:
                new_messages.append(merged_message)
                merged_message = None
            new_messages.append(message)

    if merged_message is not None:
        new_messages.append(merged_message)

    thread.messages = new_messages

    return thread


SNIPPET_REMOVED_FROM_CONTEXT = """<code_block>
<file_name>{file_name}</file_name>
<source>
Contents not shown as the file is not in the code_entity_relationship_map.
</source>
</code_block>"""

FILE_REMOVED_FROM_CONTEXT = """<file_contents>
<file_path>{file_name}</file_path>
<content>
File contents not shown as the file is not in the code_entity_relationship_map.
</content>
</file_contents>"""

RIPGREP_RESULT_REMOVED_FROM_CONTEXT = """Ripgrep results removed as the file {file_name} is not in the code_entity_relationship_map."""


def get_latest_code_entity_relationship_map(thread: Thread):
    """
    Fetches latest code_entity_relationship_map from thread messages
    Returns code_entity_relationship_map and index of the message containing the code_entity_relationship_map
    """
    code_entity_relationship_map: str | None = ""
    code_entity_relationship_map_index: int = -1
    for index, message in enumerate(thread.messages):
        if (
            index > 2 and message.role == "assistant"
        ):  # earliest code_entity_relationship_map is at index 3
            code_entity_relationship_map_dict, failed, _ = (
                extract_object_fields_from_string(
                    message.content or "", ["code_entity_relationship_map"]
                )
            )
            if not failed:
                code_entity_relationship_map = code_entity_relationship_map_dict.get("code_entity_relationship_map", "")  # type: ignore
                code_entity_relationship_map_index = index
    return code_entity_relationship_map, code_entity_relationship_map_index


def file_searcher_dynamic_context_cleanup(
    user_request: str, thread: Thread, llm_state: LLMState
):
    """
    Dynamically cleans up search agent context while it is iterating and searching through the codebase.
    """
    # first get the latest code_entity_relationship_map - we will use this to drop results from the vector search and view file results
    code_entity_relationship_map, code_entity_relationship_map_index = (
        get_latest_code_entity_relationship_map(thread)
    )
    # if code_entity_relationship_map:
    #     breakpoint()
    # if a code_entity_relationship_map is found, we can now remove all vector search and view file results where the file name is not in the latest code_entity_relationship_map
    # if user request > 10k characters, dedupe it
    if len(user_request) > 10_000:
        user_request_indices = [
            idx
            for idx, message in enumerate(thread.messages)
            if message.role == "user" and user_request in message.content
        ]
        if len(user_request_indices) > 1:
            for index in user_request_indices[:-1]:
                thread.messages[index].content = thread.messages[index].content.replace(
                    user_request, USER_REQUEST_PLACEHOLDER
                )
    if code_entity_relationship_map:
        # loop through messages again up till the index of the latest code_entity_relationship_map and 2 messages before that
        for index, message in enumerate(
            thread.messages[3 : max(code_entity_relationship_map_index - 2, 3)]
        ):
            # handle vector search tool
            tool = vector_search
            if f"{tool.name}_results" in (message.content or ""):  # type: ignore
                result_snippets, failed = extract_objects_from_string(
                    message.content or "", "snippet", ["file_name"]
                )
                if not failed:
                    for snippet_dict in result_snippets:
                        try:
                            snippet_file_name = snippet_dict["file_name"].split(":")[0]
                            if snippet_file_name not in code_entity_relationship_map:
                                # remove snippet from context
                                raw_text = snippet_dict["raw_text"]["snippet"]
                                file_name = snippet_dict["file_name"]
                                if message.content is None:
                                    message.content = ""
                                message.content = message.content.replace(
                                    raw_text,
                                    SNIPPET_REMOVED_FROM_CONTEXT.format(
                                        file_name=file_name
                                    ),
                                )
                        except Exception as e:
                            logger.warning(
                                f"failed to remove snippet from context: {e}"
                            )
            # handle access file tool
            tool = access_file
            if f"{tool.name}_results" in message.content:  # type: ignore
                result_files, failed = extract_objects_from_string(
                    message.content or "", f"{tool.name}_results", ["file_path"]
                )
                if not failed:
                    for file_dict in result_files:
                        try:
                            file_name = file_dict["file_path"].split(":")[0]
                            if file_name not in code_entity_relationship_map:
                                # remove file from context
                                raw_text = file_dict["raw_text"][f"{tool.name}_results"]
                                file_name = file_dict["file_path"]
                                if message.content is None:
                                    message.content = ""
                                message.content = message.content.replace(
                                    raw_text,
                                    FILE_REMOVED_FROM_CONTEXT.format(
                                        file_name=file_name
                                    ),
                                )
                        except Exception as e:
                            logger.warning(f"failed to remove file from context: {e}")
            # handle ripgrep tool
            tool = ripgrep
            if f"{tool.name}_results" in message.content:  # type: ignore
                ripgrep_results, failed = extract_objects_from_string(
                    message.content or "", f"{tool.name}_results", ["ripgrep_response"]
                )
                if not failed:
                    for ripgrep_dict in ripgrep_results:
                        try:
                            ripgrep_content: str = ripgrep_dict[
                                "ripgrep_response"
                            ].split("```")[1]
                            file_names: list[str] = list(
                                re.findall(
                                    r"^[^\s0-9.:-][^\s]*\.[^\s]+",
                                    ripgrep_content,
                                    re.MULTILINE,
                                )
                            )
                            file_names = [
                                file_name.strip()
                                for file_name in file_names
                                if file_name.strip()
                            ]
                            new_content = []
                            current_file = ""
                            skip_file = False
                            for line in ripgrep_content.split("\n"):
                                if line.strip() in file_names:
                                    current_file = line.strip()
                                    if "Ripgrep results removed as the file" in line:
                                        continue
                                    if current_file not in code_entity_relationship_map:
                                        skip_file = True
                                        new_content.append(
                                            RIPGREP_RESULT_REMOVED_FROM_CONTEXT.format(
                                                file_name=current_file
                                            )
                                        )
                                    else:
                                        skip_file = False
                                        new_content.append(line)
                                elif not skip_file:
                                    new_content.append(line)

                            new_ripgrep_content = "\n".join(new_content)
                            if message.content is None:
                                message.content = ""
                            message.content = message.content.replace(
                                ripgrep_content, new_ripgrep_content
                            )
                        except Exception as e:
                            ripgrep_content = ripgrep_dict.get("ripgrep_response", "")
                            logger.warning(
                                f"failed to remove ripgrep result from context: {e} ripgrep content is: {ripgrep_content}"
                            )
    return thread


def construct_snippet_from_definition(definition: Definition) -> Snippet:
    if not definition.contents:
        return None
    return Snippet(
        content=definition.contents,
        start=definition.start_line,
        end=definition.end_line,
        file_path=definition.file_path,
        score=1.0,
        type_name="source",  # TODO: classify this correctly
    )


def is_good_entity_to_match(entity: Entity) -> bool:
    if entity.contents.count("\n") < 2:  # if the entity is too small
        return False
    # typically we'll have both the definition (the full logic) and the import (1 line) so filter out imports
    if "definition.import" in entity.type:
        return False
    return True


def get_definitions_in_query(
    question: str, definitions_index: dict[str, list[Entity]]
) -> list[Definition]:
    definitions = []
    # make sure to split on whitespace
    potential_keywords = question.split()

    for potential_keyword in potential_keywords:
        # keyword too short
        if len(potential_keyword) < 9:
            continue
        matching_entities = definitions_index.get(potential_keyword, [])
        for matching_entity in matching_entities:
            if is_good_entity_to_match(matching_entity):
                definitions.append(matching_entity)
    
    return definitions


def get_entities_from_snippets(
    snippets: list[Snippet],
    entities_index: EntitiesIndex,
) -> list[Entity]:
    entities = []
    for snippet in snippets:
        file_entities = entities_index.entities_mapping[snippet.file_path]
        for file_entity in file_entities.definitions.values():
            if (
                file_entity.start_line >= snippet.start
                and file_entity.end_line <= snippet.end
                and file_entity.entity_type != "import"
                and file_entity.scope == "global"
            ):
                entities.append(file_entity)
    return entities


def changed_relationship_map(relationship_map: str) -> bool:
    if not relationship_map:
        return False
    if (
        "unchanged" in relationship_map
        and len(relationship_map.strip().splitlines()) < 3
    ):
        return False
    return True


@streamable
def file_searcher(
    username: str,
    question: str,
    cloned_repo: ClonedRepo,
    messages: list[Message] = [],
    existing_snippets: list[Snippet] = [],
    model=LATEST_CLAUDE_MODEL,
    use_case: UseCase = "ticket",
):
    yield "Sweep Search is starting...", existing_snippets, []
    thread: Thread = Thread.from_system_message_string(
        prompt_string=file_search_agent_system_message.render(use_case=use_case), model=model
    )
    user_request: str = question.strip("\n")
    thread.messages += messages  # TODO: make this acutally work
    instructions = (
        file_search_agent_instructions
        + file_searcher_tools_available
        + "\n\n"
        + example_tool_calls_file_searcher
    )
    # thread.messages.append(UserMessage(content=file_search_agent_instructions + file_searcher_tools_available + "\n\n" + example_tool_calls_file_searcher))

    if (
        use_case != "chat" and DEV and existing_snippets
    ):  # and use_instant_reply(question, existing_snippets): # TODO: add use_instant_reply back later, right now too many false negatives
        return existing_snippets

    # Directory Summaries
    directory_summaries_string = ""
    directory_summaries, directory_counts = recursively_summarize_directory(cloned_repo)
    directory_summaries_to_display = sorted(
        directory_counts.items(), key=lambda x: x[1], reverse=True
    )
    directory_summaries_to_display = [
        directory
        for directory, _ in directory_summaries_to_display
        if directory in directory_summaries
    ]
    truncated_directory_summaries = pack_items_for_prompt(
        iterable=directory_summaries_to_display,
        string_function=lambda directory: directory_summaries.get(directory, ""),
        token_limit=5_000,
    )
    for directory in truncated_directory_summaries:
        directory_summaries_string += (
            f"{directory}\n{directory_summaries[directory]}\n\n"
        )
    directory_summaries_string = directory_summaries_string.strip("\n")
    repo_summary, directory_tree = summarize_frameworks(cloned_repo)

    with Timer("entities Index"):
        entities_index = EntitiesIndex.from_dir(
            cloned_repo.repo_dir, key=cloned_repo.cache_key
        )
    # entities = get_entities_from_snippets(existing_snippets, entities_index)
    mentioned_files = []
    # list of snippets
    if not existing_snippets:
        definitions_in_query = get_definitions_in_query(
            question, entities_index.definitions_index
        )
        for definition in definitions_in_query:
            snippet = construct_snippet_from_definition(definition)
            if snippet:
                existing_snippets.append(snippet)

        mentioned_files = get_all_snippets_from_query(
            query=question, cloned_repo=cloned_repo
        )
    searched_snippets = []
    for message, searched_snippets in search_codebase.stream(
        question=user_request,
        cloned_repo=cloned_repo,
        directory_summaries=directory_summaries,
    ):
        yield message, mentioned_files + existing_snippets + searched_snippets, [] # type: ignore
    existing_snippets = mentioned_files + existing_snippets + searched_snippets
    existing_snippets = organize_snippets(existing_snippets)

    # this is better as a jinja template
    relevant_files = deepcopy(existing_snippets)
    existing_context_string = ""
    summary_string = "Here are the currently accessed contents:\n"
    for index, snippet in enumerate(existing_snippets):
        snippet_content = snippet.get_snippet(add_lines=False, add_ellipsis=False)
        if snippet.start <= 1 and snippet.end == len(snippet.content.splitlines()):
            snippet_name = f"{snippet.file_path} (full file)"
            existing_snippet = existing_file_format.format(
                index=index, file_path=snippet.file_path, source=snippet_content
            )
        else:
            snippet_name = f"{snippet.file_path}:{snippet.start}-{snippet.end}"
            existing_snippet = existing_snippet_format.format(
                index=index, file_path=snippet_name, source=snippet_content
            )
        summary_string += f"- {snippet_name}"
        if ":" not in snippet_name:
            summary_string += " (full file)"
        summary_string += "\n"
        existing_context_string += f"{existing_snippet}\n"
    summary_string = summary_string.strip("\n")
    # longer than necessary, needs to be optimized to be shorter
    user_message = file_search_agent_user_message.format(
        repo=cloned_repo.repo_full_name,
        directory_tree=directory_tree,
        directory_summaries=directory_summaries_string,
        repo_summary=repo_summary,
        existing_context=existing_context_string,
        summary=summary_string,
        instructions=instructions,
        user_request=question,
        user_request_analysis=(
            first_message_user_instructions
            if len(thread.messages) <= 1
            else follow_up_user_instructions
        ),
    )
    user_message = user_message.strip("\n")

    if thread.messages[-1].content.strip("\n") == question.strip("\n"):
        # remove the last message from the thread messages, it will be repeated
        thread.messages.pop()

    # user_message += file_search_agent_code_entity_relationship_map_initialisation
    llm_state = LLMState(
        request=question,
        visited_snippets=set(),
        visited_questions=set(),
        visited_ripgrep=set(),
        ripgrep_queries=set(),
        viewed_files=set(),
        entities_index=entities_index,
    )
    # list of function calls made as messages to let the user know what is happening
    function_calls_messages: list[Message] = []
    # clean up context
    thread = file_searcher_context_cleanup(thread)
    early_exit_reason = "Exited early due to max iterations reached"
    # number of iterations search agent is allowed
    FILE_SEARCHER_MAX_ITERS = 6
    for iter_num in range(FILE_SEARCHER_MAX_ITERS):
        yield f"Sweep search is running...", relevant_files, function_calls_messages
        # clean up context from unused tool call results
        thread = file_searcher_dynamic_context_cleanup(user_request, thread, llm_state)
        # list of all function calls made
        function_calls: list[AnthropicFunctionCall] = []
        function_calls_response = {}
        try:
            for (
                thinking,
                function_calls_response,
                function_calls,
            ) in get_multi_function_calls.stream(
                username,
                thread,
                user_message,
                file_searcher_tools,
                llm_kwargs={"model": model},
                cloned_repo=cloned_repo,
                llm_state=llm_state,
                relevant_files=relevant_files,
            ):
                # list of all function calls made as messages to let the user know what is happening
                # this should be reset every iteration
                all_function_calls_as_messages: list[Message] = []
                tags_to_replace = {
                    "<existing_context_examination>": "",
                    "</existing_context_examination>": "",
                    "<scratchpad>": "",
                    "</scratchpad>": "",
                    "<reflection>": "",
                    "</reflection>": "",
                    "<sub_requests>": "# Plan\n",
                    "</sub_requests>": "",
                    "<stack_analysis>": "# Repo Summary\n",
                    "</stack_analysis>": "",
                    "<planned_tool_calls>": "# Tool Calls\n",
                    "</planned_tool_calls>": "",
                    "<planning>": "# Planning\n",
                    "</planning>": "",
                    "<context_analysis>": "# Context Analysis\n",
                    "</context_analysis>": "",
                    "<user_request_analysis>": "",
                    "</user_request_analysis>": "",
                }
                # for tag in tags_to_remove:
                for tag, replacement in tags_to_replace.items():
                    thinking = thinking.replace(tag, replacement)
                function_key_suffix = "_multi" if len(function_calls) > 1 else "_single"
                all_function_calls_as_messages.append(
                    Message(
                        role="function",
                        content="",
                        function_call={
                            "function_name": "deciding",
                            "function_parameters": "",
                            "is_complete": False,
                            "thinking": thinking,
                        },
                        key="function_call" + function_key_suffix,
                    )
                )
                if not function_calls:
                    yield "Sweep is thinking...", relevant_files, function_calls_messages + all_function_calls_as_messages
                tools_string = ""
                # iterate through all the function calls and add them to the function_calls_messages
                for index, function_call in enumerate(function_calls):
                    function_call_message: Message = get_function_call_message_base(
                        function_call={
                            "function_name": function_call.function_name,
                            "function_parameters": function_call.function_parameters,
                        },
                        key="function_call_output" + function_key_suffix,
                    )
                    if function_calls_response.get("results", []):
                        current_function_call_result = function_calls_response.get(
                            "results", []
                        )[index]
                    else:
                        current_function_call_result = ""
                    snippets = (
                        []
                        if function_call.function_name != "vector_search"
                        else parse_file_names(current_function_call_result, cloned_repo)
                    )
                    if snippets:
                        function_call_message.function_call["snippets"] = snippets
                    if function_calls_response:
                        function_call_message.content = current_function_call_result
                    all_function_calls_as_messages.append(function_call_message)
                    tools_string = ", ".join(
                        [
                            f"{function_call.function_name}"
                            for function_call in function_calls
                        ]
                    )
                if function_calls:
                    yield f"Sweep is calling the following tools:\n{tools_string}", relevant_files, function_calls_messages + all_function_calls_as_messages
                function_calls_response_string = format_multi_function_call_results(
                    username,
                    thread,
                    function_calls_response,
                    function_calls,
                )
                function_calls_response_string = function_calls_response_string.strip()
        except BadRequestError as e:
            # break early if we ran out of context and attempt to answer the user's request with the current context
            # This is for anthropic native
            if "is too long" in e.body.get("error", {}).get("message", ""):
                early_exit_reason = "Exited early due to overflown context"
                break
        # check for general AWS error
        except Exception as e:
            if "is too long" in str(e):
                early_exit_reason = "Exited early due to overflown context"
                break
        
        
        # if iter_num >= 1:
        #     bp()

        if function_calls:
            relationship_map = ""
            for message in thread.messages[::-1]:
                parsed_relationship_map, _ = extract_objects_from_string(
                    message.content, "code_entity_relationship_map"
                )
                if parsed_relationship_map:
                    relationship_map = parsed_relationship_map[-1]["content"]
                    if relationship_map:
                        break
            if not relationship_map:
                logger.warning("[YELLOW] No relationship map found")
            function_calls_response_string += (
                "\n\n"
                + subsequent_search_instructions.render(
                    relationship_map=relationship_map, user_request=user_request
                )
            )

        yield f"Sweep is processing the tool outputs...", relevant_files, function_calls_messages + all_function_calls_as_messages
        function_calls_messages.extend(all_function_calls_as_messages)

        yield f"Sweep is processed the tool outputs...", relevant_files, function_calls_messages

        # if iter_num >= 2:
        #     breakpoint()

        if len(function_calls_response.get("results", [])) == 1:
            user_message = f"Here is the output for the tool you called:\n<tool_call_outputs>\n{function_calls_response_string}\n</tool_call_outputs>\nExamine the output above and determine your next steps."
        else:
            user_message = f"Here are the outputs for the tools you called:\n<tool_calls_outputs>\n{function_calls_response_string}\n</tool_calls_outputs>\nExamine the outputs above and determine your next steps."
        
        # for catching duplicated function calls
        # if len(function_calls) >= 6:
        #     breakpoint()

        # see if we finish by see if done_file_search was called
        if any(function_call.function_name == "done_file_search" for function_call in function_calls):
            yield "Sweep Search is done...", relevant_files, function_calls_messages
            return relevant_files

    # if we reach here than we have reached the max number of iterations
    # dump current existing context to snippets and use that as the context
    # breakpoint()
    code_entity_relationship_map, _code_entity_relationship_map_index = (
        get_latest_code_entity_relationship_map(thread)
    )
    # mock a done_file_search tool call
    done_file_search(
        reason=early_exit_reason,
        code_entity_relationship_map=code_entity_relationship_map,
        existing_patterns="",
        relevant_files=relevant_files,
        cloned_repo=cloned_repo,
        llm_state=llm_state,
    )
    # create the corresponding message for the done_file_search tool call
    mock_function_parameters = {
        "reason": early_exit_reason,
        "code_entity_relationship_map": code_entity_relationship_map,
        "existing_patterns": "",
    }
    final_done_file_search_message = get_function_call_message_base(
        content=code_entity_relationship_map,
        function_call={
            "function_name": done_file_search.name,
            "function_parameters": mock_function_parameters,
            "is_complete": True,
            "thinking": "Search Agent wasn't able to complete fully, returning the current context",
        },
        key="function_call_output_single",
    )
    posthog.capture(
        "file_searcher" "file_searcher max_iters_reached",
        properties={
            "username": username,
            "question": user_request,
            "repo": cloned_repo.repo_full_name,
            "model": model,
            "code_entity_relationship_map": code_entity_relationship_map,
        },
    )

    function_calls_messages.append(final_done_file_search_message)
    yield "Sweep Search is done...", relevant_files, function_calls_messages
    return relevant_files


if __name__ == "__main__":
    pass
    # go to # tests/agents/test_search_agent.py for tests
