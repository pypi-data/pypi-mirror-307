from loguru import logger

from sweepai.backend.api_utils import (
    get_pr_snippets,
)
from sweepai.core.entities import (
    AssistantMessage,
    Message,
    Snippet,
    SystemMessage,
    UserMessage,
)
from sweepai.core.github_utils import ClonedRepo
from sweepai.core.llm.chat import LATEST_CLAUDE_SONNET_MODEL, Thread, continuous_llm_calls
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.dataclasses.code_change_stream_state import CodeChangeStreamState
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.core.entities import organize_snippets
from sweepai.modify.quick_modify import format_changes
from sweepai.modify.modify_utils import find_best_matches
from sweepai.modify.validate.code_validators import (
    remove_placeholder_comments_from_code,
)
from sweepai.o11y.event_logger import posthog
from sweepai.o11y.log_utils import log_to_file
from sweepai.o11y.posthog_trace import posthog_trace
from sweepai.search.agent.search_prompts import (
    o1_preview_fix_ci_message,
    anthropic_solve_problem_format_message,
    anthropic_conclusion_format,
    anthropic_fix_ci_conclusion_prompt,
    anthropic_fix_ci_message,
    anthropic_fix_ci_selection_prompt,
    anthropic_follow_up_prefix,
    anthropic_format_message,
    anthropic_system_message,
    assistant_prefill_message_for_code_suggestions,
    relevant_snippets_message,
    search_agent_existing_patterns_prompt,
    search_agent_solution_prompt,
)
from sweepai.utils.str_utils import (
    extract_fenced_code_blocks,
    extract_object_fields_from_string,
    extract_xml_tag,
    get_hash,
)
from sweepai.utils.streamable_functions import streamable


def preprocess_messages(messages):
    code_entity_relationship_map = ""
    search_agent_solution = ""
    existing_patterns = ""
    search_solution_message = messages[-1]
    if search_solution_message.role == "function" and search_solution_message.function_call:
        code_entity_relationship_map_dict, failed, _ = extract_object_fields_from_string(
            search_solution_message.function_call.get("thinking", ""),
            ["code_entity_relationship_map"],
        )
        if not failed:
            code_entity_relationship_map = code_entity_relationship_map_dict.get("code_entity_relationship_map", "").strip()  # type: ignore
        else:  # if code_entity_relationship_map is not fetched it may not be in the last message but the ones before, fetch the latest code_entity_relationship_map
            # find the latest code_entity_relationship_map
            for message in reversed(messages):
                if message.role == "function" and message.function_call:
                    code_entity_relationship_map_dict, failed, _ = extract_object_fields_from_string(
                        message.function_call.get("thinking", ""),
                        ["code_entity_relationship_map"],
                    )
                    if not failed:
                        code_entity_relationship_map = code_entity_relationship_map_dict.get("code_entity_relationship_map", "").strip()  # type: ignore
                    if code_entity_relationship_map:
                        break
        try:
            search_agent_solution = (
                search_solution_message.function_call.get("function_parameters", {}).get("solution", "").strip()
            )
        except Exception as e:
            logger.warning(f"Error during search agent solution extraction: {e}")
            search_agent_solution = ""
        try:
            existing_patterns = (
                search_solution_message.function_call.get("function_parameters", {})
                .get("existing_patterns", "")
                .strip()
            )
        except Exception as e:
            logger.warning(f"Error during existing patterns extraction: {e}")
            existing_patterns = ""
    return (
        code_entity_relationship_map,
        search_agent_solution,
        existing_patterns,
        messages,
    )


# TODO: port the tracking ID over to the chat agent
@streamable
@posthog_trace
def chat_agent(
    username: str,
    cloned_repo: ClonedRepo,
    messages: list[Message],
    modify_files_dict: dict,
    snippets: list[Snippet],
    context: ChatAgentContext,
    metadata: dict = {},
):
    tracking_id = metadata.get("tracking_id", get_hash())
    cleaned_repo_name = cloned_repo.repo_full_name.replace("/", "--")
    file_identifier = f"chat-agent-{username}-{cleaned_repo_name}-{tracking_id}"
    logger.info(f"Logs redirected to {file_identifier}")
    with log_to_file(file_identifier):
        model = LATEST_CLAUDE_SONNET_MODEL
        # model = "gpt-4o"
        if not snippets:
            raise ValueError("No snippets were sent.")
        repo_name = cloned_repo.repo_full_name
        system_message = (
            anthropic_system_message.render(use_case=context.use_case)
        )  # TODO: handle this better
        # go backward through the messages until we get a user message with role == 'user'
        initial_user_message = ""
        for message in reversed(messages):
            if message.role == "user":
                initial_user_message = message.content or ""
                break
        if initial_user_message == "":
            raise ValueError("Something went wrong! No user message was found in the messages.")
        thread: Thread = Thread.from_system_message_string(prompt_string=system_message)
        # make a copy of the messages to avoid modifying the original

        pr_snippets = []
        # remove function calls for the following tools
        messages = list(
            filter(
                lambda message: not (
                    (
                        message.role == "function"
                        and message.function_call.get("function_name", "")
                        in (
                            "vector_search",
                            "add_files_to_context",
                            "done_file_search",
                            "access_file",
                            "ripgrep",
                        )
                    )
                    or (hasattr(message, "content") and message.content.strip() == "")
                ),
                messages,
            )
        )
        # parsing logic for funtion calls
        all_pulls_messages = ""
        pr_snippets_for_rendering_ci_prompts = []
        for message in messages:
            if message.role == "user":
                message.content = message.content.strip()
            elif message.role == "function":
                message.role = "user"
                function_name = message.function_call.get("function_name", "")
                if function_name == "done_file_search":
                    message.content = message.function_call.get("function_parameters", {}).get("solution", "")
                elif function_name == "ripgrep":
                    message.content = message.content.split("First, think step-by-step in a scratchpad")[0]
                    message.content = message.content.replace("<ripgrep_response>", "")
            if message.function_call:
                message.function_call = None  # pass certain validations
            if message.annotations:
                new_pr_snippets, skipped_pr_snippets, pulls_messages = get_pr_snippets(
                    repo_name,
                    message.annotations,
                    cloned_repo,
                    context=context,
                )
                pr_snippets_for_rendering_ci_prompts = new_pr_snippets + skipped_pr_snippets
                pr_snippets = organize_snippets(pr_snippets + new_pr_snippets)
                if pulls_messages:
                    all_pulls_messages += pulls_messages.rstrip() + "\n\n"
                    message.content += (
                        "\n\nPull requests:\n"
                        + pulls_messages
                        + f"\n\nBe sure to summarize the contents of the pull request during the analysis phase separately from other relevant files.\n\nRemember, the user's request was:\n\n<message>\n{message.content}\n</message>"
                    )

        relevant_pr_snippets: list[Snippet] = []
        other_relevant_snippets: list[Snippet] = []
        if pr_snippets:
            for snippet in snippets:
                if snippet.file_path in [pr_snippet.file_path for pr_snippet in pr_snippets]:
                    relevant_pr_snippets.append(snippet)
                else:
                    other_relevant_snippets.append(snippet)

        snippets_message = relevant_snippets_message.render(
            repo_name=repo_name,
            relevant_snippets=snippets,
            relevant_pr_snippets=relevant_pr_snippets,
            other_relevant_snippets=other_relevant_snippets,
        )

        thread.messages = [
            SystemMessage(content=thread.messages[0].content),
            UserMessage(content=snippets_message),
            # *[message for message in messages[:-1] if message.content != "Loading..."], # Dropping this as part of an experiment to reduce context
        ]

        if all_pulls_messages:
            thread.messages.append(
                UserMessage(
                    content=all_pulls_messages,
                )
            )

        search_agent_solution = metadata.get("search_agent_solution", "")
        code_entity_relationship_map = metadata.get("code_entity_relationship_map", "")
        existing_patterns = metadata.get("existing_patterns", "")
        # append the latest search solution message to the end of the messages
        if search_agent_solution or code_entity_relationship_map:
            formatted_search_agent_prompt = ""
            if search_agent_solution:
                formatted_search_agent_prompt += search_agent_solution_prompt.format(
                    search_agent_solution=search_agent_solution
                )
            # unsure how to solve for when the code_entity_relationship_map is unchanged probably need to check when metadata is entered
            if existing_patterns:
                formatted_search_agent_prompt += search_agent_existing_patterns_prompt.format(
                    existing_patterns=existing_patterns
                )
            thread.messages.append(UserMessage(content=formatted_search_agent_prompt, key="search_agent_solution"))

        thread.messages.append(
            UserMessage(
                content=anthropic_follow_up_prefix.render(
                    user_request=initial_user_message,
                    use_case=context.use_case,
                    history=context.history,
                )
            )
        )

        rewritten_solution = ""
        if context.use_case == "ci":
            # get the assistant's reply with the problem solving format (automatically appended to the thread)
            # this is also a great spot to do validation via another LLM call
            if model.startswith("o1-"):
                __o1_preview_fix_ci_message_response = continuous_llm_calls(
                    username,
                    thread,
                    content=o1_preview_fix_ci_message.render(
                        pr_files=pr_snippets_for_rendering_ci_prompts,
                        use_case=context.use_case,
                        history=context.history,
                    ),
                    stop_sequences=["</analysis>"],
                    model="o1-preview",
                )

                anthropic_fix_ci_conclusion_prompt_response = continuous_llm_calls(
                    username,
                    thread,
                    content=anthropic_fix_ci_conclusion_prompt,
                    stop_sequences=["</rewritten_solution>"],
                    model=model,
                )
                rewritten_solution = extract_xml_tag(anthropic_fix_ci_conclusion_prompt_response, "rewritten_solution", include_closing_tag=False)
                rewritten_solution = remove_placeholder_comments_from_code(
                    rewritten_solution
                )
                logger.info(f"REWRITTEN SOLUTION:\n{rewritten_solution}")

                thread.messages = thread.messages[:-4]
                # breakpoint()
            else:
                __anthropic_fix_ci_message_response = continuous_llm_calls(
                    username,
                    thread,
                    content=anthropic_fix_ci_message.render(
                        pr_files=pr_snippets_for_rendering_ci_prompts,
                        use_case=context.use_case,
                        history=context.history,
                    ),
                    stop_sequences=["</analysis>", "</format>"],
                    model=model,
                )
                logger.debug(f"Suggestions: {__anthropic_fix_ci_message_response}")
                __anthropic_fix_ci_selection_prompt_response = continuous_llm_calls(
                    username,
                    thread,
                    content=anthropic_fix_ci_selection_prompt.render(
                        pr_files=pr_snippets_for_rendering_ci_prompts,
                        use_case=context.use_case,
                        history=context.history,
                    ),
                    stop_sequences=["</best_fix_selection>", "</format>"],
                    model=model,
                )
                logger.debug(f"Selection: {__anthropic_fix_ci_selection_prompt_response}")
                anthropic_fix_ci_conclusion_prompt_response = continuous_llm_calls(
                    username,
                    thread,
                    content=anthropic_fix_ci_conclusion_prompt,
                    stop_sequences=["</rewritten_solution>"],
                    model=model,
                )
                rewritten_solution = extract_xml_tag(anthropic_fix_ci_conclusion_prompt_response, "rewritten_solution", include_closing_tag=False)
                rewritten_solution = remove_placeholder_comments_from_code(
                    rewritten_solution
                )  # remove placeholder comments from here only
                # remove the fix_ci_message and fix_ci_selection_prompt from the thread
                logger.info(f"REWRITTEN SOLUTION:\n{rewritten_solution}")
                # breakpoint() # Really good spot to put a breakpoint
                # Delete 6 because we have 3 calls * 2 messages, this resets the context
                thread.messages = thread.messages[:-6]
        elif False: # experimental
            __anthropic_solve_problem_format_message_response = continuous_llm_calls(
                username,
                thread,
                content=anthropic_solve_problem_format_message.render(use_case=context.use_case),
                model="o1-preview",
            )
            rewritten_solution = remove_placeholder_comments_from_code(rewritten_solution)
            logger.info(f"REWRITTEN SOLUTION:\n{rewritten_solution}")

        user_message = (
            anthropic_format_message.render(use_case=context.use_case)
            + "\n\n"
            + anthropic_conclusion_format.render(user_request=initial_user_message, proposed_solution=rewritten_solution)
        )
        new_messages: list[Message] = []
        # convert this to a FileModificationState
        code_stream_modify_files_dict = FileModificationState()
        previous_modify_files_dict: dict = metadata.get("modify_files_dict", {})
        for file_path, file_content in previous_modify_files_dict.items():
            code_stream_modify_files_dict.add_or_update_file(file_path, file_content["contents"], file_content["contents"])

        modify_files_dict: FileModificationState = FileModificationState.from_dict(previous_modify_files_dict)

        # use this to manage the state of the stream when generating code suggestions
        code_change_stream_state: CodeChangeStreamState = CodeChangeStreamState(
            username=username,
            model=model,
            cloned_repo=cloned_repo,
            thread=thread,
            stop_sequences=["</user_response>"],
            modify_files_dict=code_stream_modify_files_dict,
        )

        yield new_messages

        request_assistant_message_content = assistant_prefill_message_for_code_suggestions.render(context=context)
        user_response = ""
        result_string = ""
        current_messages = []
        for result_string in code_change_stream_state.stream(
            user_message,
            request_assistant_message_content,
        ):
            if len(result_string) < 200:  # preamble
                continue
            code_change_stream_state.update_state_with_new_response(result_string)
            analysis = extract_xml_tag(result_string, "analysis", include_closing_tag=False) or ""
            user_response = extract_xml_tag(result_string, "user_response", include_closing_tag=False) or ""
            if analysis or user_response:
                current_messages = []

                if analysis:
                    current_messages.append(
                        Message(
                            content=analysis,
                            role="function",
                            function_call={
                                "function_name": "analysis",
                                "function_parameters": {},
                                "is_complete": bool(user_response),
                            },
                        )
                    )

                if user_response:
                    current_messages.append(AssistantMessage(content=user_response, annotations={}))

                yield [*new_messages, *current_messages]
            else:
                current_messages = [AssistantMessage(content=result_string, annotations={})]
                yield [*new_messages, *current_messages]

        new_messages.extend(current_messages)
        if rewritten_solution:
            new_messages[-1].content = (
                "## Thinking\n\n" + rewritten_solution + "\n\n## Suggestion\n\n" + new_messages[-1].content
            )

        yield new_messages

        message_content: str = new_messages[-1].content

        # EXTRACTING CODE ANNOTATIONS
        code_fence_blocks = extract_fenced_code_blocks(message_content)
        snippet_code_matches: dict[str, dict[str, list[dict[str, str]]]] = {}
        for code_content, code_data in code_fence_blocks.items():
            if code_data.get("language", "") != "diff":
                code_matches: dict[str, list[dict[str, str]]] = {}
                # get fuzzy match based on current snippet context
                for snippet in snippets:
                    try:
                        best_matches = find_best_matches(
                            code_content,
                            snippet.content,
                            threshold=90,
                            tokenized=True,
                            context=2,
                        )
                        for match in best_matches:
                            matched_code, score, start, end = match
                            if snippet.file_path not in code_matches:
                                code_matches[snippet.file_path] = []
                            snippet_match = {
                                "code": matched_code,
                                "start": start,
                                "end": end,
                                "score": score,
                                "language": code_data.get("language", ""),
                            }
                            code_matches[snippet.file_path].append(snippet_match)
                    except Exception as e:
                        logger.error(f"Error finding best matches: {e}")
                        continue
                snippet_code_matches[code_content] = code_matches
        if snippet_code_matches:
            if not hasattr(new_messages[-1], "annotations") or new_messages[-1].annotations is None:
                new_messages[-1].annotations = {}
            # Now you can safely assign snippet_code_matches
            new_messages[-1].annotations["snippetCodeMatches"] = snippet_code_matches
            yield new_messages

        code_change_stream_state.apply_last_code_change()
        modify_files_dict = code_change_stream_state.modify_files_dict
        assert len(modify_files_dict) or context.use_case == "chat"

        modify_files_dict = format_changes(modify_files_dict, cloned_repo)
        # # EXTRACTING CODE SUGGESTIONS
        # code_suggestions = extract_and_clean_code_suggestions(message_content, cloned_repo)
        # logger.info(f"Code Suggestions:\n{render_code_suggestions_for_logging(code_suggestions)}")

        # # VALIDATING CODE SUGGESTIONS
        # file_change_requests, current_content = validate_code_suggestions(
        #     code_suggestions, cloned_repo, modify_files_dict, new_messages[-1].content
        # )
        # new_messages[-1].annotations["codeSuggestions"] = code_suggestions
        # new_messages[-1].content = current_content

        # ## NEW MODIFY START
        # parsed_code_suggestions = [CodeSuggestion.from_camel_case(code_suggestion) for code_suggestion in code_suggestions]
        # new_modify_files_dict = quick_modify(parsed_code_suggestions, cloned_repo, modify_files_dict)

        # new_messages[-1].annotations["codeSuggestions"] = new_modify_files_dict.to_raw_code_suggestions()
        new_messages[-1].annotations["codeSuggestions"] = modify_files_dict.to_raw_code_suggestions()

        assert new_messages[-1].annotations["codeSuggestions"] or context.use_case == "chat"
        yield new_messages

        ## MODIFY END

        posthog.capture(
            metadata["username"],
            "chat_codebase complete",
            properties={
                **metadata,
                "messages": [message.model_dump() for message in messages],
            },
        )
