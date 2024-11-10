import copy

from loguru import logger

from sweepai.core.entities import FileChangeRequest, Message
from sweepai.core.github_utils import ClonedRepo
from sweepai.core.llm.chat import Thread, continuous_llm_calls
from sweepai.core.llm.convert_openai_anthropic import AnthropicFunctionCall
from sweepai.dataclasses.code_suggestions import StatefulCodeSuggestion
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.dataclasses.llm_state import ModifyLLMState
from sweepai.modify.modify_prompts import LINTER_WARNING_PROMPT
from sweepai.modify.modify_utils import (
    MODEL,
    NO_TOOL_CALL_PROMPT,
    SLOW_MODEL,
    SUBMIT_TASK_MOCK_FUNCTION_CALL,
    changes_made,
    compile_fcr,
    create_user_message,
    get_current_task_index,
    get_replaces_per_fcr,
    handle_function_call,
    instructions,
    modify_tools,
    render_current_task,
    render_plan,
    tasks_completed,
    validate_and_parse_function_call,
)
from sweepai.modify.validate.code_validators import format_file
from sweepai.utils.diff import generate_diff
from sweepai.utils.streamable_functions import Streamable, streamable


def generate_code_suggestions(
    modify_files_dict: FileModificationState,
) -> list[StatefulCodeSuggestion]:
    applied_code_suggestions = []
    for file_path in sorted(modify_files_dict.files):
        if modify_files_dict.file_has_changes(file_path):
            applied_code_suggestions.append(
                StatefulCodeSuggestion(
                    file_path=file_path,
                    original_code=modify_files_dict.get_original_contents(file_path),
                    new_code=modify_files_dict.get_new_contents(file_path),
                    file_contents=modify_files_dict.get_original_contents(file_path),
                    state="done",
                )
            )
    return applied_code_suggestions


modify_stop_sequences = [
    "</make_change>",
    "</create_file>",
    "</submit_task>",
    "</function_call>",
]


@streamable
def modify(
    fcrs: list[FileChangeRequest],
    request: str,
    cloned_repo: ClonedRepo,
    relevant_filepaths: list[str],
    previous_modify_files_dict: FileModificationState = FileModificationState(),
    raise_on_max_iterations: bool = False,
) -> Streamable[dict[str, dict[str, str]]]:
    # join fcr in case of duplicates
    # handles renames in cloned_repo
    # TODO: handle deletions here - it can cause crashes
    if not fcrs:
        return previous_modify_files_dict
    user_message = create_user_message(
        fcrs=fcrs,
        request=request,
        cloned_repo=cloned_repo,
        relevant_filepaths=relevant_filepaths,
        modify_files_dict=previous_modify_files_dict,
    )
    thread = Thread()
    llm_state: ModifyLLMState = ModifyLLMState(
        initial_check_results={},
        done_counter=0,
        request=request,
        plan=render_plan(fcrs),
        current_task=render_current_task(fcrs),
        user_message_index=1,
        user_message_index_chat_logger=1,
        fcrs=fcrs,
        previous_attempt="",
        changes_per_fcr=[get_replaces_per_fcr(fcr) for fcr in fcrs],
        completed_changes_per_fcr=[0 for _ in fcrs],
        attempt_lazy_change=True,
        attempt_count=0,
        visited_set=set(),
        status_messages=[],
        symbol_to_code_map={},
    )
    full_instructions = instructions + modify_tools
    thread.messages = [Message(role="system", content=full_instructions)]
    try:
        if compiled_fcr := compile_fcr(fcr=fcrs[0], index=0, cloned_repo=cloned_repo):
            thread.messages.append(
                Message(
                    role="user",
                    content=f"Here is the initial user request, plan, and state of the code files:\n{user_message}",
                )
            )
            function_calls_string = compiled_fcr
            thread.messages.append(
                Message(role="assistant", content=function_calls_string)  # this will happen no matter what
            )
            # update messages to make it seem as if it called the fcr
            # update state if it's bad
            # TODO: handling logic to be moved out
            function_call: AnthropicFunctionCall = validate_and_parse_function_call(
                function_calls_string, thread
            )  # this will raise if it's bad but compile_fcr should guarantee it's good
        else:
            model = MODEL
            logger.info(f"Using model: {model}")
            file_names = ", ".join([fcr.filename for fcr in fcrs])
            logger.warning(
                f"[YELLOW] Unexpected LLM call: Calling LLM from modifying with model {model} for files: {file_names}"
            )
            function_calls_string = continuous_llm_calls(
                "initial modify",
                thread,
                content=f"Here is the initial user request, plan, and state of the code files:\n{user_message}",
                model=model,
                stop_sequences=modify_stop_sequences,
            )
    except Exception as e:
        logger.error(f"Error in chat_anthropic: {e}")
        return {}
    modify_files_dict = copy.deepcopy(previous_modify_files_dict)
    # this message list is for the chat logger to have a detailed insight into why failures occur
    detailed_chat_logger_messages = [{"role": message.role, "content": message.content} for message in thread.messages]
    # used to determine if changes were made
    previous_modify_files_dict = copy.deepcopy(modify_files_dict)

    for i in range(max(len(fcrs), 5)):
        yield generate_code_suggestions(modify_files_dict)
        function_call = validate_and_parse_function_call(function_calls_string, thread)
        if function_call:
            num_of_tasks_done = tasks_completed(fcrs)
            # note that detailed_chat_logger_messages is meant to be modified in place by handle_function_call
            function_output, modify_files_dict, llm_state = handle_function_call(
                cloned_repo,
                function_call,
                modify_files_dict,
                llm_state,
                chat_logger_messages=detailed_chat_logger_messages,
            )
            logger.info(function_output)
            fcrs = llm_state.fcrs
            if function_output == "DONE":
                # add the diff of all changes to chat_logger
                break
            # bp()
            detailed_chat_logger_messages.append({"role": "user", "content": function_output})

            if modify_files_dict:  # update the state of the LLM
                user_message = create_user_message(
                    fcrs=fcrs,
                    request=request,
                    cloned_repo=cloned_repo,
                    relevant_filepaths=relevant_filepaths,
                    modify_files_dict=modify_files_dict,
                )
                user_message = f"Here is the UPDATED user request, plan, and state of the code changes. REVIEW THIS CAREFULLY!\n{user_message}"
                # state cleanup should only occur after a task has been finished and if a change was made and if a change was made
                current_num_of_tasks_done = tasks_completed(fcrs)
                if (
                    changes_made(modify_files_dict, previous_modify_files_dict)
                    and current_num_of_tasks_done > num_of_tasks_done
                ):
                    # remove the previous user message and add it to the end, do not remove if it is the inital user message
                    thread.messages = thread.messages[:1]
                    detailed_chat_logger_messages = detailed_chat_logger_messages[:1]
                    thread.messages.append(Message(role="user", content=user_message))
                    detailed_chat_logger_messages.append({"role": "user", "content": user_message})
                    # update the index
                    llm_state.user_message_index = len(thread.messages) - 1
                    llm_state.user_message_index_chat_logger = len(detailed_chat_logger_messages) - 1
                previous_modify_files_dict = copy.deepcopy(modify_files_dict)
        else:
            function_output = NO_TOOL_CALL_PROMPT
        try:
            function_calls_string = ""
            compiled_fcr = ""
            current_fcr_index = get_current_task_index(fcrs)
            change_in_fcr_index = llm_state.completed_changes_per_fcr[current_fcr_index]
            max_changes = llm_state.changes_per_fcr[current_fcr_index]
            if change_in_fcr_index >= max_changes:
                function_calls_string = SUBMIT_TASK_MOCK_FUNCTION_CALL.format(
                    justification=f"Task {current_fcr_index} is now complete."
                )
            else:
                # on first attempt of a new task we use the first fcr
                if llm_state.attempt_lazy_change:
                    if compiled_fcr := compile_fcr(fcrs[current_fcr_index], change_in_fcr_index, cloned_repo):
                        function_calls_string = compiled_fcr
                        function_call = validate_and_parse_function_call(
                            function_calls_string, thread
                        )  # this will raise if it's bad but compile_fcr should guarantee it's good
                        logger.info(f"Function call:\n{function_call}")
                        # update messages to make it seem as if it called the fcr
                        thread.messages.append(Message(role="assistant", content=function_calls_string))
                # if previous things go wrong we make llm call
                if not function_calls_string:
                    if LINTER_WARNING_PROMPT in function_output:
                        llm_state.attempt_count = 3  # skip to opus if there is a linter warning
                    model = MODEL if llm_state.attempt_count < 3 else SLOW_MODEL
                    file_names = ", ".join([fcr.filename for fcr in fcrs])
                    logger.warning(
                        f"Unexpected LLM call: Calling LLM from modifying with model {model} for files: {file_names}"
                    )
                    function_calls_string = continuous_llm_calls(
                        "attempt fix modify",
                        thread,
                        content=function_output,
                        model=model,
                        stop_sequences=modify_stop_sequences,
                    )
                    if function_calls_string in llm_state.visited_set:
                        if llm_state.attempt_count < 3:
                            logger.warning(
                                f"Function call {function_calls_string} has already been visited, retrying with a different model."
                            )
                            llm_state.attempt_count = 3
                            function_calls_string = continuous_llm_calls(
                                "fallback modify",
                                thread,
                                content=function_output,
                                model=model,
                                stop_sequences=modify_stop_sequences,
                            )
                            if function_calls_string in llm_state.visited_set:
                                logger.warning(
                                    f"Function call {function_calls_string} has already been visited, skipping task {current_fcr_index}."
                                )
                                function_calls_string = SUBMIT_TASK_MOCK_FUNCTION_CALL.format(
                                    justification=f"Skipping task {current_fcr_index} due to too many retries."
                                )
                            else:
                                llm_state.visited_set = set()
                        else:
                            logger.warning(
                                f"Function call {function_calls_string} has already been visited, skipping task {current_fcr_index}."
                            )
                            function_calls_string = SUBMIT_TASK_MOCK_FUNCTION_CALL.format(
                                justification=f"Skipping task {current_fcr_index} due to too many retries."
                            )
        except Exception as e:
            logger.error(f"Error in chat_anthropic: {e}")
            with open("msg.txt", "w") as f:
                for message in thread.messages:
                    f.write(f"{message.content}\n\n")
            break
    else:
        logger.error("Max iterations reached")
        if raise_on_max_iterations:
            raise Exception("Max iterations reached")
    for file_path in modify_files_dict.files:
        # this is the diff count of the original code and the formatted code (will be big if the customer doesn't typically using a formatter)
        original_contents = modify_files_dict.get_original_contents(file_path)
        formatted_original_contents = format_file(file_path, original_contents, cloned_repo.repo_dir)
        # if the diff is small, then the original code was already formatted
        original_code_formatted = len(generate_diff(original_contents, formatted_original_contents)) < 10
        if original_code_formatted:  # if the original code was formatted
            formatted_new_contents = format_file(
                file_path,
                modify_files_dict.get_new_contents(file_path),
                cloned_repo.repo_dir,
            )
            modify_files_dict.update_new_contents(file_path, formatted_new_contents)

    diff_string = ""
    for file_name in modify_files_dict.files:
        if diff := generate_diff(
            modify_files_dict.get_original_contents(file_name),
            modify_files_dict.get_new_contents(file_name),
        ):
            diff_string += f"\nChanges made to {file_name}:\n{diff}"
    logger.info(
        "\n".join(
            generate_diff(
                modify_files_dict.get_original_contents(file_name),
                modify_files_dict.get_new_contents(file_name),
            )
            for file_name in modify_files_dict.files
        )
    )  # adding this as a useful way to render the diffs
    yield generate_code_suggestions(modify_files_dict)
    return modify_files_dict


if __name__ == "__main__":
    pass
