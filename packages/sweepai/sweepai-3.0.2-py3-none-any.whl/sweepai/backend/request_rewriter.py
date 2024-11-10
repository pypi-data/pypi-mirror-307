"""
Changelog:

09.30.2024 - I made huge changes to make it much more concise and not bias the search agent towards an incorrect answer type.

09.30.2024 - I removed the What Should be Done section and also removed the line of "include ALL items in the codebase that needs to be found" because it would trick search agent into making bad queries like
Class.method instead of class_instance.method
"""

from loguru import logger

from sweepai.backend.api_utils import get_pr_snippets
from sweepai.core.github_utils import ClonedRepo, MockClonedRepo
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread, continuous_llm_calls
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.core.entities import organize_snippets
from sweepai.search.agent.agent_utils import (
    get_all_snippets_from_query,
    search_codebase,
)
from sweepai.search.agent.entity_search import EntitiesIndex
from sweepai.search.agent.search_agent import (
    construct_snippet_from_definition,
    existing_file_format,
    existing_snippet_format,
    get_definitions_in_query,
)
from sweepai.search.agent.summarize_directory import (
    recursively_summarize_directory,
    summarize_frameworks,
)
from sweepai.utils.format_utils import Prompt
from sweepai.utils.str_utils import pack_items_for_prompt
from sweepai.utils.streamable_functions import streamable
from sweepai.utils.timer import Timer

system_message = Prompt(
    """You are a senior engineer at Google, known for clear and concise communication. {% if use_case == "chat" %}Your task is to refine user questions about the {{repo}} repository.{% else %}Your task is to refine user requests for code changes in the {{repo}} repository.{% endif %}"""
)

user_message = Prompt(
    """\
<context>
<!-- Use this context to rewrite the user's request -->
<repository>
<!-- The name of the GitHub repository -->
{{repo}}
</repository>

<repository_summary>
<!-- An overall summary of the repository, including its purpose and tech stack -->
{{repo_summary}}
</repository_summary>

<directory_tree>
<!-- The file structure of the repository -->
{{directory_tree}}
</directory_tree>

<directory_summaries>
<!-- Summaries of key directories in the repository -->
{{directory_summaries}}
</directory_summaries>

<summary>
<!-- A brief summary of the currently accessed contents -->
{{summary}}
</summary>

<existing_context>
<!-- Relevant code snippets or files that have been accessed -->
{{existing_context}}
</existing_context>
</context>

Guidelines:
{%- if use_case == "chat" %}
1. Include a concise overview for all code snippets you need to find in the codebase.
2. Use concise language for easier readability.
3. Use GitHub-style markdown, enclosing file paths and code symbols in backticks.
4. Maximize readability by adding line breaks and whitespace where appropriate.
{% else %}
1. Include an extremely concise overview of the necessary code changes and tests to be added.
2. Use numbered lists with entries such as "In FILE, make the following changes."
3. Be specific in the location and nature of code changes but not in the implementation details.
4. Do not suggest running tests or installing dependencies.
5. Do not update documentation unless the user mentions to do so.
6. Do not suggest changes to packages, modules, or configurations.
7. Use concise language and maximize readability.
8. Use GitHub-style markdown, enclosing file paths and code symbols in backticks.
9. Tests should pass on the first try. Do not say "Ensure tests pass" because it's assumed that they will.
{% endif %}
Rewriting Instructions:
- Preserve text in quotation marks ("") or backticks (`) exactly as is.
- Integrate preserved quoted text seamlessly into the new context.
- Use triple backticks (```) for code blocks and single backticks (`) for inline code or error messages.

Output Format:

<new_ticket>
# [Concise Title]
## Description:
{% if use_case == "chat" %}
[Brief description of the code snippets to be found]

## Tasks:

- [Clarify what you will search for]
...

## [Additional tasks if necessary]
{% else %}
[Brief description of the changes to be made]

## Task:

- [Clarify what you will work on]

## Test (if requested/applicable):

- [Test case 1]
- [Test case 2]
...

## [Additional tasks if necessary]
{% endif %}
</new_ticket>

Example:

<new_ticket>
{%- if use_case == "chat" %}
# Where do we cache existing usernames during login?

## Tasks:

- Trace the implementation of the FastAPI login endpoint in `src/router.py`
- Identify the underlying database queries by following the function calls
- Identify the cache mechanism used based on these queries
{% else %}
# Implement user authentication in login module

## Description:
Add user authentication functionality to the login module, including password hashing, JWT token generation, and input validation.

## Tasks:

- Update `src/auth/login.py` to include user authentication logic
    - Add password hashing
    - Implement JWT token generation

## Test:

- Add unit tests in `tests/auth/test_login.py`
    - Successful login
    - Failed login with incorrect password
    - Input validation for empty fields
{% endif -%}
</new_ticket>

Now, rewrite the following user request with added clarity and specificity based on the provided context:

<user_request>
{{user_request}}
</user_request>"""
)


@streamable
def rewrite_query(
    username: str,
    question: str,
    cloned_repo: ClonedRepo,
    pulls: list[dict],
    model=LATEST_CLAUDE_MODEL,
    context: ChatAgentContext = ChatAgentContext(),
):
    user_request: str = question.strip("\n")

    existing_snippets = []
    yield "Processing pull request data...", "", []
    if pulls:
        pulls_messages = ""
        existing_snippets, _, pulls_messages = get_pr_snippets(
            cloned_repo.repo_full_name, {"pulls": pulls}, cloned_repo, context=context
        )
        if pulls_messages.count("<pull_request>") > 1:
            pulls_messages = (
                "\n\nHere are the mentioned pull request(s) already written relevant to the user's query:\n\n"
                + pulls_messages
            )

        user_request = pulls_messages + "\n\n" + user_request

    # Directory Summaries
    yield "Getting directory summaries...", "", []
    directory_summaries_string = ""
    directory_summaries, directory_counts = recursively_summarize_directory(cloned_repo)
    directory_summaries_to_display = sorted(directory_counts.items(), key=lambda x: x[1], reverse=True)
    directory_summaries_to_display = [
        directory for directory, _ in directory_summaries_to_display if directory in directory_summaries
    ]
    truncated_directory_summaries = pack_items_for_prompt(
        iterable=directory_summaries_to_display,
        string_function=lambda directory: directory_summaries.get(directory, ""),
        token_limit=5_000,
    )
    for directory in truncated_directory_summaries:
        directory_summaries_string += f"{directory}\n{directory_summaries[directory]}\n\n"
    directory_summaries_string = directory_summaries_string.strip("\n")
    repo_summary, directory_tree = summarize_frameworks(cloned_repo)

    entities_index = EntitiesIndex.from_dir(
        cloned_repo.repo_dir,
        key=f"{cloned_repo.repo_full_name}:{cloned_repo.current_commit_sha}",
    )
    definitions_in_query = get_definitions_in_query(question, entities_index.definitions_index)
    for definition in definitions_in_query:
        snippet = construct_snippet_from_definition(definition)
        if snippet:
            existing_snippets.append(snippet)

    mentioned_files = get_all_snippets_from_query(query=question, cloned_repo=cloned_repo)
    # only resort to vector searching the question if no mentioned files or existing snippets exist
    searched_snippets = []
    for message, searched_snippets in search_codebase.stream(
        question=user_request,
        cloned_repo=cloned_repo,
        directory_summaries=directory_summaries,
    ):
        yield message, "", mentioned_files + existing_snippets + searched_snippets
    existing_snippets = mentioned_files + existing_snippets + searched_snippets
    existing_snippets = organize_snippets(existing_snippets)

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
        summary_string += "\n"
        existing_context_string += f"{existing_snippet}\n"
    summary_string = summary_string.strip("\n")
    with Timer():
        thread = Thread.from_system_message_string(
            system_message.render(repo=cloned_repo.repo_full_name, use_case=context.use_case)
        )
        formatted_user_message = user_message.render(
            repo=cloned_repo.repo_full_name,
            existing_context=existing_context_string,
            summary=summary_string,
            repo_summary=repo_summary,
            directory_tree=directory_tree,
            directory_summaries=directory_summaries_string,
            user_request=user_request,
            use_case=context.use_case,
        )
        for response in continuous_llm_calls.stream(
            username,
            thread,
            content=formatted_user_message,
            stop_sequences=["</new_ticket>"],
            model=model,
        ):
            if "<new_ticket>" in response:
                _, new_ticket_description = response.split("<new_ticket>")
                new_ticket_description = new_ticket_description.strip().removesuffix("</new_ticket>").strip()
                yield "", new_ticket_description, mentioned_files + existing_snippets
            else:
                # try splitting on <new_ticket>
                if (
                    len(response) < 300
                ):  # preamble where <new_ticket> is not present so we don't want to incorrectly say ERROR
                    # I yield a space to indicate new_ticket_description is non-null which prepends the original request in the outer scope
                    yield "", " ", mentioned_files + existing_snippets
                # If there is no <new_ticket> in the response after 40 characters, then we should tell the user
                # This is an error state so we should tell the user
                else:
                    yield "", f"ERROR: Sweep failed to rewrite the query.\n\n {response}", []


if __name__ == "__main__":
    import os

    from sweepai.config.server import CACHE_DIRECTORY

    QUERY = os.environ.get(
        "QUERY",
        "when on_ticket or on_comment fail, we should tell the user that it's not their fault\n\nadd a mailto:support@sweep.dev with a placeholder subject and text and prompt them to click this.\nadd this only on failure",
    )
    REPO = os.environ.get("REPO", "sweepai/sweep-internal")
    COMMIT_SHA = os.environ.get("COMMIT_SHA", "base/dev")
    with Timer():
        for message, new_ticket, snippets in rewrite_query.stream(
            "username",
            QUERY,
            MockClonedRepo(
                _repo_dir=f"{CACHE_DIRECTORY}/repos/{REPO}/{COMMIT_SHA}",
                repo_full_name=REPO,
            ),
            pulls=[],
            context=ChatAgentContext(
                history="",
                ci_step=False,
            ),
        ):
            pass
        logger.info("\n\n" + new_ticket + "\n\n")
