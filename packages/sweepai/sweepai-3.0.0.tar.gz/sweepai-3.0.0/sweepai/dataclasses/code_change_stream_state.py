import os
import re
from dataclasses import dataclass, field
from typing import Generator, Optional, Tuple

from loguru import logger

from sweepai.core.entities import Message
from sweepai.core.github_utils import ClonedRepo, MockClonedRepo
from sweepai.core.llm.chat import (
    LATEST_CLAUDE_MODEL,
    Thread,
    collapse_final_assistant_messages,
    continuous_llm_calls,
)
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.search.agent.code_tree import CodeTree
from sweepai.search.agent.snippet_utils import merge_snippet_ranges
from sweepai.utils.diff import generate_diff
from sweepai.utils.str_utils import (
    extract_lines,
    find_match_line_index,
    find_match_with_leading_spaces,
    reset_rightmost_string,
    should_truncate,
    strip_triple_quotes_preserve_whitespace,
    truncate,
)

MIN_LINES_FOR_BOUNDARY_TRUNCATION = 300
MAX_STREAM_CHANGES = 60
STREAM_VERSION = 2


def truncate_on_boundary(haystack: str, needle: str, language: str) -> str:
    start_index = find_match_line_index(haystack, needle)

    if start_index == -1:
        return ""

    end_index = start_index + len(needle.splitlines())

    try:
        code_tree = CodeTree.from_code(haystack, language=language)
    except Exception as e:
        logger.warning(f"Could not parse code tree for language {language}:\n{str(e)}")
        return ""
    boundaries = code_tree.get_boundaries()
    for boundary in boundaries:
        suggestion_is_long_enough = boundary - start_index > MIN_LINES_FOR_BOUNDARY_TRUNCATION
        if start_index <= boundary <= end_index and suggestion_is_long_enough:
            return extract_lines(haystack, start_index, boundary).strip("\n")
    return ""


def postprocessed_truncate_on_boundary(haystack: str, needle: str, language: str):
    boundary_truncated_code = truncate_on_boundary(haystack, needle, language)
    if boundary_truncated_code:
        boundary_truncated_code += "\n```\n</original_code>\n<new_code>\n```"
        return boundary_truncated_code
    return ""

def strip_partial_closing_tags(code: str) -> str:
    tag = "```\n</original_code>"
    while not code.endswith(tag):
        tag = tag[:-1]
    if len(tag) > len("```\n</or"):
        code = code.removesuffix(tag)
    return code

END_OF_ORIGINAL_CODE_MARKER = "```\n</original_code>\n<new_code>\n```"

def get_replacement_original_code(current_file_contents: str, partial_original_code: str) -> str:
    # If we should truncate, we return new right side. Otherwise, returns empty string.
    if should_truncate(current_file_contents, partial_original_code):
        logger.info("Truncating original code")
        truncated_code = truncate(current_file_contents, partial_original_code) # make this handle indentation changes
        if truncated_code:
            *_, remaining_code = current_file_contents.split(truncated_code, 1)
        else:
            # the first line of code is nowhere to be found in the file
            remaining_code = current_file_contents
            # breakpoint() # Good spot for breakpoint
        remaining_code = remaining_code.removeprefix("\n") # removes first newline
        if remaining_code:
            shortest_non_whitespace_substring = ""
            for line in remaining_code.splitlines():
                # Inject up to the first non-whitespace line
                shortest_non_whitespace_substring += line + "\n"
                if line.strip() and len(truncated_code) + len(shortest_non_whitespace_substring) > len(partial_original_code):
                    break
            replacement_original_code = ""
            shortest_non_whitespace_substring = shortest_non_whitespace_substring.rstrip("\n")
            if not shortest_non_whitespace_substring:
                replacement_original_code += END_OF_ORIGINAL_CODE_MARKER
            else:
                if shortest_non_whitespace_substring == remaining_code:
                    # This hit end of file so we should stop the original code
                    shortest_non_whitespace_substring += "\n" + END_OF_ORIGINAL_CODE_MARKER
                if truncated_code:
                    replacement_original_code = truncated_code + "\n" + shortest_non_whitespace_substring
                else:
                    replacement_original_code = shortest_non_whitespace_substring
        else:
            # file is complete
            replacement_original_code = truncated_code + "\n" + END_OF_ORIGINAL_CODE_MARKER
        return replacement_original_code
    return ""

def detect_infinite_loop_in_code_in_suggested_responses(all_suggested_responses: list[str]) -> bool:
    """
    Detects if the model is stuck in an infinite loop generating code suggestions. We will check if a certain state occurs >= 3 times.
    """
    code_suggestion_to_count = {}
    for suggested_response in all_suggested_responses:
        if suggested_response not in code_suggestion_to_count:
            code_suggestion_to_count[suggested_response] = 1
        else:
            code_suggestion_to_count[suggested_response] += 1
        if code_suggestion_to_count[suggested_response] >= 3:
            return True
    return False

@dataclass
class PartialCodeChange:
    """
    A partial code change that is generated by the model, only file_path is required
    """

    file_path: str
    raw_match: str
    justification: Optional[str] = None
    original_code: Optional[str] = None
    new_code: Optional[str] = None
    completed: bool = False
    generating_original_code: bool = False
    generating_new_code: bool = False

    def __eq__(self, other):
        if not isinstance(other, PartialCodeChange):
            return NotImplemented

        return (
            self.file_path == other.file_path
            and self.raw_match == other.raw_match
            and self.justification == other.justification
            and self.original_code == other.original_code
            and self.new_code == other.new_code
            and self.completed == other.completed
            and self.generating_original_code == other.generating_original_code
            and self.generating_new_code == other.generating_new_code
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(
            (
                self.file_path,
                self.raw_match,
                self.justification,
                self.original_code,
                self.new_code,
                self.completed,
                self.generating_original_code,
                self.generating_new_code,
            )
        )

    def __repr__(self):
        # print if completed
        # if completed, print "Completed" and the diff
        # otherwise print the original code and new code so far
        if self.completed and self.original_code and self.new_code:
            return "Completed" + generate_diff(old_code=self.original_code, new_code=self.new_code)
        return f"Not Completed:\nOriginal Code:\n{self.original_code}\nNew Code:\n{self.new_code}"


@dataclass
class CodeChangeStreamState:
    """
    Specialized state management for generating code changes
    """

    # if we can find a way to remove the following two fields, we should, we need to to call continuous_llm_calls after consuming the suggested response
    username: str
    model: str

    # we need all the below fields
    cloned_repo: ClonedRepo
    thread: Thread
    current_file_path: str = ""  # Path to the file that is being generated
    starting_response: str = ""  # Starting response from the model (to compare against the current_response)
    current_response: str = (
        ""  # Current response from the model (expected to be partially generated as it is being streamed)
    )
    suggested_response: str = (
        ""  # Suggested response to the model based on the current_response (the entire assistant message)
    )
    modify_files_dict: FileModificationState = field(default_factory=FileModificationState)
    code_change_partial_regex: str = (
        r"<code_change>\s*<file_path>\n*(?P<filePath>[\s\S]+?)\n*</file_path>\s*(<justification>\n*(?P<justification>[\s\S]+?)\n*(</justification>)?)?\s*(<original_code>\n*(?P<originalCode>[\s\S]*?\s*)(</original_code>)?\n*)?(<new_code>\n*(?P<newCode>[\s\S]+?)\n*(</new_code>)?)?\s*($|</code_change>|</original_code>|</new_code>)"
    )
    error_message: str = ""  # Error message to be displayed to the user
    partial_code_change: Optional[PartialCodeChange] = None
    applied_code_changes: set[PartialCodeChange] = field(default_factory=set)  # set of previously applied changes
    _all_suggested_responses: list[str] = field(default_factory=list)

    # also try and get rid of these fields too since the only reason we need them is for continuous_llm_calls
    stop_sequences: list[str] = field(default_factory=list)

    # Additional fields for detecting large negative diffs
    large_negative_diff_threshold: float = 0.2  # 20% of the file deleted
    last_generated_diff_was_large_deletion: bool = False  # Flag to track if the last diff was large
    last_large_deletion_diff_file_path: str = ""  # File path of the last large deletion diff
    last_validated_code_change: PartialCodeChange | None = None

    def get_latest_contents(self, file_path: str, safe: bool = False) -> str:
        """
        Get the latest contents of the file based on the modify_files_dict, this should be how you fetch the latest contents of a file
        """
        try:
            if file_path in self.modify_files_dict:
                return self.modify_files_dict.get_new_contents(file_path)
            return self.cloned_repo.get_file_contents(os.path.normpath(file_path))
        except FileNotFoundError as e:
            if safe:
                return ""
            raise e

    def get_partial_code_changes(self) -> list[PartialCodeChange]:
        """
        Get the partial code changes based on the current_response
        """
        partial_code_changes: list[PartialCodeChange] = []
        for match in re.finditer(self.code_change_partial_regex, self.current_response):
            raw_match = match.group(0)
            file_path = match.group("filePath")
            # this is the safe way to default these values, and I've only defaulted these three and not file_path because that's a fatal error
            justification = match.group("justification") or ""
            original_code = match.group("originalCode") or ""
            new_code = match.group("newCode") or ""
            generating_original_code = "<original_code>" in raw_match and "```\n</origin" not in raw_match # full match sometimes is insufficient
            generating_new_code = "<new_code>" in raw_match and "</new_code>" not in raw_match
            completed = "</code_change>" in raw_match
            # do some post processing on the fields
            if file_path:
                file_path = file_path.strip()
            if original_code and generating_original_code:
                # use strip_triple_quotes to remove the triple quotes from the original code
                original_code = strip_triple_quotes_preserve_whitespace(original_code)
            if new_code:
                new_code = strip_triple_quotes_preserve_whitespace(new_code)

            if completed:
                original_code = strip_triple_quotes_preserve_whitespace(original_code).strip("\n")
                new_code = strip_triple_quotes_preserve_whitespace(new_code).strip("\n")
            partial_code_changes.append(
                PartialCodeChange(
                    file_path=file_path,
                    raw_match=raw_match,
                    justification=justification,
                    original_code=original_code,
                    new_code=new_code,
                    completed=completed,
                    generating_original_code=generating_original_code,
                    generating_new_code=generating_new_code,
                )
            )
        return partial_code_changes

    def handle_early_update_state_exit(self):
        """
        Properly handle an early exit from update_state_with_new_response, this MUST BE CALLED before you return in the function
        """
        self.suggested_response = ""
        self.current_file_path = ""
        self.partial_code_change = None

    def detect_large_negative_diff(self, file_path: str, original_code: str, new_code: str) -> bool:
        """
        Detects if applying new_code to file_path would result in a large negative diff.

        Args:
            file_path (str): Path to the file being modified.
            new_code (str): The proposed new code to apply.

        Returns:
            bool: True if a large negative diff is detected, False otherwise.
        """
        try:
            current_file_contents = self.get_latest_contents(file_path)
            if original_code not in current_file_contents:
                # TODO: This is a fatal error, we should handle this better
                logger.error(f"Original code not found in {file_path}. Cannot detect large negative diff.")
                return False
            replaced_file_contents = current_file_contents.replace(original_code, new_code)
            # Compute the diff
            diff = generate_diff(current_file_contents, replaced_file_contents)
            total_lines = len(current_file_contents.splitlines())
            deleted_lines = 0
            for line in diff:
                if line.startswith("-") and not line.startswith("---"):
                    deleted_lines += 1
                elif line.startswith("+") and not line.startswith("+++"):
                    deleted_lines -= 1
            # Calculate the percentage of lines deleted
            if total_lines == 0:
                return False
            deletion_percentage = deleted_lines / total_lines
            if deletion_percentage > self.large_negative_diff_threshold or deleted_lines > 40:
                logger.warning(
                    f"Large negative diff detected for {file_path}: {deleted_lines} ({deletion_percentage*100:.2f}%) lines deleted."
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Error detecting large negative diff for {file_path}: {e}")
            return False

    def generate_reset_new_code(self, file_path: str):
        """
        Resets the new_code by deleting all code until the last tag and starting over.

        Args:
            file_path (str): Path to the file being modified.
        """
        try:
            # Find the last occurrence of <new_code> tag
            last_new_code_tag = self.current_response.rfind("<new_code>")
            if last_new_code_tag == -1:
                # this is actually an error, but we should never hit this case
                logger.error(f"<new_code> tag not found in {file_path}. Cannot reset new_code.")
                return ""
            # Delete all code until the last <new_code> tag
            reset_content = self.current_response[:last_new_code_tag]
            # Append the opening <new_code> tag to start fresh
            reset_content += "<new_code>\n```"
            logger.info(f"Reset new_code for {file_path}.")
            return reset_content
        except Exception as e:
            logger.error(f"Error resetting new_code for {file_path}: {e}")
            return ""

    def validate_deletion_diffs_and_suggest_response(self, file_path: str):
        """
        Handles scenarios when a large negative diff is detected.

        Args:
            file_path (str): Path to the file being modified.
            new_code (str): The proposed new code to apply.
        """
        if self.detect_large_negative_diff(
            file_path=file_path,
            original_code=self.partial_code_change.original_code,
            new_code=self.partial_code_change.new_code,
        ):
            # Skip validation in two cases
            # Case 1: If the last generated diff was a large deletion and the current one is similar
            # Case 2: Checked the same file path twice (ensures we make progress)
            if self.last_generated_diff_was_large_deletion or self.last_large_deletion_diff_file_path == file_path:
                # Accept the large negative diff as it's similar to the previous one
                logger.info(f"Accepting large negative diff for {file_path} as the model has generated this twice.")
                self.last_generated_diff_was_large_deletion = False  # Reset flag
            else:
                # Reset the new_code and set the flag
                self.suggested_response = self.generate_reset_new_code(file_path)
                # Set these two fields so if we encounter the same one, we'll accept it
                self.last_generated_diff_was_large_deletion = True
                self.last_large_deletion_diff_file_path = file_path
        else:
            self.last_generated_diff_was_large_deletion = False  # Reset flag

    def check_if_suggested_code_is_at_end_of_file(self, file_contents: str, suggested_code: str) -> str:
        """
        Check if the suggested_code is at the end of the file. Returns the trailing string that follows the suggested_code if it is at the end of the file
        """
        rstripped_file_contents = file_contents.rstrip()
        # if the suggested code is at the end of the file, update the suggested code to include the rest of the file
        if rstripped_file_contents.endswith(suggested_code.rstrip()) and file_contents.count(suggested_code) == 1:
            match_index = file_contents.index(suggested_code)
            matched_content = file_contents[match_index + len(suggested_code) :]
            trailing_content = f"{matched_content}\n```\n</original_code>"
            return trailing_content
        return ""

    def try_generate_original_code_with_entities(self, partial_original_code: str) -> str:
        """
        Attempt to generate the original code based on the entities in the file
        """
        MIN_ENTITY_SUGGESTION_LENGTH = 30
        MAX_ENTITY_SUGGESTION_LENGTH = 100  # when suggesting entities, we want to limit the length of the suggestion
        # note: during this experiment I decreased from 300 to 100. then i decreased from 100 to 50. because it leads to too many problems when you suggest huge chunks of code
        # having it be so long causes the LLM to delete code because original code is so long.
        language = self.current_file_path.split(".")[-1]
        current_file_contents = self.get_latest_contents(self.current_file_path)
        rest_of_original_code_to_suggest = ""
        try:
            # check if an entities in the code file match against the partial code change
            tree = CodeTree.from_code(current_file_contents, language=language)
            # could be optimized by calling a specially created function to only get the entities with the code already filled in but this works for now
            entities_spans = tree.get_entities_spans()
            if entities_spans:
                import_line_ranges = tree.get_import_line_ranges()
                merged_import_ranges = merge_snippet_ranges(import_line_ranges, context_lines=5)
                current_file_contents_lines = current_file_contents.splitlines()

                for start_line, end_line in merged_import_ranges:
                    entities_spans[start_line] = end_line

                matched_start_line = find_match_line_index(
                    current_file_contents, partial_original_code
                )  # -1 if not found so this is safe
                matched_end_line = matched_start_line + len(partial_original_code.splitlines())

                for line_index in range(matched_start_line, matched_end_line):
                    if line_index in entities_spans:
                        predicted_end_line = entities_spans[line_index]
                        if (
                            predicted_end_line > matched_end_line
                            and MIN_ENTITY_SUGGESTION_LENGTH
                            < predicted_end_line - matched_end_line
                            < MAX_ENTITY_SUGGESTION_LENGTH
                        ):
                            # if line_index != matched_start_line:
                            # bp()
                            prev_lines = current_file_contents_lines[matched_start_line:line_index]
                            next_lines = current_file_contents_lines[line_index : predicted_end_line + 1]
                            rest_of_original_code_to_suggest = "\n".join(prev_lines + next_lines).strip("\n")
                            break

        except Exception as e:
            logger.warning(f"Could not parse code tree for file {self.current_file_path}:\n{str(e)}")
        return rest_of_original_code_to_suggest

    def fill_original_code_by_double_newline(self, partial_original_code: str) -> str:
        """
        Fills the original code by finding the next double newline
        """
        MIN_LINES_NEEDED_FOR_SUGGESTION = 10
        SUGGESTED_LINES = 50  # this is ideally the number of lines we want to suggest
        MAX_NAIVE_SUGGESTED_LINES = 150  # this is the maximum number of lines we can suggest naively
        current_file_contents = self.get_latest_contents(self.current_file_path)
        match_index = current_file_contents.index(partial_original_code)
        # this should just be the next tree-sitter node but we'll use double newline for now
        # Include the actual match and the following lines
        matched_content = current_file_contents[match_index + len(partial_original_code) :]
        lines = matched_content.split("\n")
        # we want the index of the furthest double newline
        next_double_newline_index = 0
        for i, line in enumerate(lines[:SUGGESTED_LINES]):
            if line.strip() == "" and i + 1 < len(lines) and len(lines[i + 1]) > 0:
                next_double_newline_index = i
        suggest_more_lines = False
        if next_double_newline_index <= MIN_LINES_NEEDED_FOR_SUGGESTION:
            next_double_newline_index = SUGGESTED_LINES
            suggest_more_lines = True
            # try again but this time with the maximum number of lines, break as soon as we can
            # it is better to suggest more and end on a double new line that to suggest less and end on a single new line
            for i, line in enumerate(lines[:MAX_NAIVE_SUGGESTED_LINES]):
                if line.strip() == "" and i + 1 < len(lines) and len(lines[i + 1]) > 0 and i > SUGGESTED_LINES:
                    next_double_newline_index = i
                    break
        suggested_lines = min(next_double_newline_index, SUGGESTED_LINES)
        if suggest_more_lines:
            suggested_lines = min(next_double_newline_index, MAX_NAIVE_SUGGESTED_LINES)
        # Take the match and up to suggested_lines after it
        result_lines = lines[: suggested_lines + 1]
        # iterate through result lines backwards and remove any lines that are pure whitespace
        for i in range(len(result_lines) - 1, -1, -1):
            if result_lines[i].strip() == "":
                result_lines.pop(i)
            else:
                break
        result = "\n".join(result_lines)
        return result

    def generate_suggested_response(self):
        """
        Attempt to generate a suggested response based on the current state
        """
        if not self.partial_code_change:
            self.handle_early_update_state_exit()
            return

        # TODO: handle missing original_code tags

        if self.partial_code_change.generating_original_code and self.partial_code_change.original_code:
            partial_original_code = self.partial_code_change.original_code
            # safe=True here because if current_file_contents is empty/nonexistent, and therefore partial_original_code is wrong, partial_original_code will be truncated, and LLM will continue to generate code as new_code
            current_file_contents = self.get_latest_contents(self.current_file_path, safe=True)
            MIN_LINES_NEEDED_FOR_SUGGESTION = 1
            # at least 2 lines of original code have to be generated before we can suggest the rest of the code, this is to prevent issues where ``` are the only thing generated
            if (
                len(self.partial_code_change.original_code.replace("`", "").splitlines())
                < MIN_LINES_NEEDED_FOR_SUGGESTION
            ):
                self.handle_early_update_state_exit()
                return

            # Try suggesting the rest of the code
            if current_file_contents:
                partial_original_code = self.validate_and_fix_partial_original_code(partial_original_code)
            else:
                # YOU ARE CREATING A NEW FILE HERE
                # if the file doesn't exist, truncate and return
                new_right_side = "\n```\n</original_code>\n<new_code>\n"
                self.suggested_response = self.current_response.rsplit(partial_original_code, 1)[0] + new_right_side
                return

            # We should truncate if the the partial original code is not in the current file contents
            if self.partial_code_change.generating_original_code and (replacement_original_code := get_replacement_original_code(current_file_contents, partial_original_code)):
                self.suggested_response = self.current_response.rsplit(partial_original_code, 1)[0] + replacement_original_code

            partial_original_code = self.validate_and_fix_partial_original_code(partial_original_code)

            # START OF ANCHOR TRUNCATION
            language = self.current_file_path.split(".")[-1]
            if boundary_truncated_code := postprocessed_truncate_on_boundary(
                current_file_contents, partial_original_code, language
            ):
                self.suggested_response = reset_rightmost_string(
                    self.current_response,
                    partial_original_code,
                    boundary_truncated_code,
                )
                # breakpoint()
                return
            # END OF ANCHOR_TRUNCATION

            # if there is a unique direct match, we can suggest the rest of the code
            original_code_to_suggest = ""
            if current_file_contents.count(partial_original_code) == 1:
                # try to generate the original code based on the entities in the file
                original_code_to_suggest = self.try_generate_original_code_with_entities(partial_original_code)
                if not original_code_to_suggest:
                    rest_of_original_code_to_suggest = self.fill_original_code_by_double_newline(partial_original_code)
                    if rest_of_original_code_to_suggest:
                        original_code_to_suggest = partial_original_code + rest_of_original_code_to_suggest

                if original_code_to_suggest:
                    if boundary_truncated_code := postprocessed_truncate_on_boundary(
                        current_file_contents, original_code_to_suggest, language
                    ):
                        original_code_to_suggest = boundary_truncated_code
                        # breakpoint()
                    original_code_to_suggest = reset_rightmost_string(
                        self.current_response,
                        partial_original_code,
                        original_code_to_suggest,
                    ).rstrip("\n")

                # final check to see if the suggested code is at the end of the file
                trailing_content = self.check_if_suggested_code_is_at_end_of_file(
                    current_file_contents, original_code_to_suggest
                )
                if trailing_content:
                    original_code_to_suggest += trailing_content
                if original_code_to_suggest:
                    self.suggested_response = original_code_to_suggest

        else:
            self.suggested_response = ""  # reset suggested response if there is nothing to suggest

    def consume_suggested_assistant_content(self) -> Tuple[str, Generator]:
        """
        Consume the suggested original code and update the state, returns a stream
        """
        suggested_original_code = self.suggested_response
        self.current_response = self.suggested_response
        self.starting_response = self.current_response
        self._all_suggested_responses.append(self.suggested_response) # used for logging and debugging
        self.suggested_response = ""
        prefilled_assistant_message = Message(content=suggested_original_code, role="assistant")
        self.thread = collapse_final_assistant_messages(self.thread)
        # if there is already an assistant message in the last spot, replace it
        # otherwise, append the new assistant message
        if self.thread.messages[-1].role == "assistant":
            self.thread.messages[-1] = prefilled_assistant_message
        else:
            self.thread.messages.append(prefilled_assistant_message)
        prefix_string = prefilled_assistant_message.content
        new_stream = continuous_llm_calls.stream(
            username=self.username,
            thread=self.thread,
            content="",  # must be empty stream for prefilled assistant message
            stop_sequences=self.stop_sequences,
            model=self.model,
            max_tokens=4096,
            __version__=STREAM_VERSION,
        )

        return prefix_string, new_stream  # type: ignore

    def apply_code_change(self, code_change: PartialCodeChange):
        if code_change.completed and code_change not in self.applied_code_changes:
            # apply updates
            file_contents_to_update = self.get_latest_contents(code_change.file_path, safe=True)
            try:
                if code_change.original_code == "":
                    # append to end
                    file_contents_to_update += f"\n\n{code_change.new_code}"
                else:
                    file_contents_to_update = file_contents_to_update.replace(
                        code_change.original_code, code_change.new_code, 1
                    )
                self.modify_files_dict.update_new_contents(code_change.file_path, file_contents_to_update)
                self.applied_code_changes.add(code_change)
            except Exception as e:
                self.error_message += f"\n\nCould not apply code change to file {code_change.file_path}:\n{str(e)}"
                logger.error(self.error_message)

    def apply_last_code_change(self):
        partial_code_changes = self.get_partial_code_changes()
        if partial_code_changes:
            self.apply_code_change(partial_code_changes[-1])

    def update_state_with_new_response(self, new_response: str):
        """
        Call this everytime a new token is generated to update the state
        """
        self.current_response = new_response

        # parse partial suggested code_changes
        partial_code_changes = self.get_partial_code_changes()

        # in the case of no partial code changes, no further state updates are necessary
        if not partial_code_changes:
            self.handle_early_update_state_exit()
            return

        # we assume that only the last code change is partially generated and all prior ones are fully complete
        # now we see if we can provide a suggested response to the model based on the latest partial code change
        self.partial_code_change = partial_code_changes[-1]

        # be strict here to keep the model in check
        has_llm_generated_any_new_tokens = len(self.current_response) - len(self.starting_response) > 0
        if not has_llm_generated_any_new_tokens:
            self.handle_early_update_state_exit()
            return

        ### VALIDATION LOGIC
        # Detect large deletion diffs before applying changes
        # We always know there's at least one partial code change at this point.
        # We can check the last index where it's completed for potential large negative diffs.
        # Use last_validated_code_change instead of an attribute on PartialCodeChange because self.partial_code_change is continuously reinstantiated
        is_partial_code_change_validated = self.last_validated_code_change == self.partial_code_change
        if self.partial_code_change.new_code and self.partial_code_change.completed and not is_partial_code_change_validated:
            self.validate_deletion_diffs_and_suggest_response(file_path=self.partial_code_change.file_path)
            if self.suggested_response:
                return
            else:
                self.last_validated_code_change = self.partial_code_change
        ### END VALIDATION LOGIC
        # if the last code change is already completed, we don't need to do anything
        if self.partial_code_change.completed:
            self.handle_early_update_state_exit()
            return

        ### HANDLE STATE UPDATES
        # PARSE CURRENT FILE PATH
        modifying_previously_unchanged_file = False
        if self.partial_code_change.file_path != self.current_file_path:
            # we have moved onto a previously unchanged file, update the file path and clear the suggested response
            self.current_file_path = self.partial_code_change.file_path
            modifying_previously_unchanged_file = True
        # see if it is in our modify_files_dict
        if modifying_previously_unchanged_file:
            if self.current_file_path not in self.modify_files_dict:
                # update modify_files_dict
                try:
                    # try to save unnecessary calls to get_latest_contents
                    current_normed_path = os.path.normpath(self.current_file_path)
                    # use safe=True because it's a new file
                    current_file_contents = self.get_latest_contents(current_normed_path, safe=True)
                    self.modify_files_dict.add_or_update_file(
                        file_path=self.current_file_path,
                        original_contents=current_file_contents,
                        new_contents=current_file_contents,
                    )
                except FileNotFoundError:
                    # we should not see this error because we're using get_latest_contents with safe=True
                    logger.error(f"File {self.current_file_path} not found")
                except Exception as e:
                    self.error_message = f"Could not get contents of file {self.current_file_path}:\n{str(e)}"
                    logger.error(self.error_message)

        # do not continue if an error has occurred
        if self.error_message:
            self.handle_early_update_state_exit()
            return

        # TODO: MORE ROBUST UPDATE MODIFIED FILES DICT BASED ON PREVIOUS CODE CHANGES
        # currently assume each change can be applied right away
        for code_change in partial_code_changes[:-1]:
            self.apply_code_change(code_change)

        if self.error_message:
            self.handle_early_update_state_exit()
            return

        # Check here after this is done, we don't want to generally early exit here because new files might be created which always have empty original_code
        current_original_code_is_empty = (not bool(self.partial_code_change.original_code)) or (
            not len(self.partial_code_change.original_code) > 0
        )
        if current_original_code_is_empty:
            self.handle_early_update_state_exit()
            return

        self.generate_suggested_response()

    def validate_and_fix_partial_original_code(self, partial_original_code: str) -> str:
        # This is bad practicd, causes side effects
        current_file_contents = self.get_latest_contents(self.current_file_path)
        # double check the indentation on the provided original_code
        # 2 cases, 1 for single line one for multi line
        spaces_needed = 0
        if len(partial_original_code.splitlines()) == 1:
            if current_file_contents.count(partial_original_code) == 1:
                match_line_index = find_match_line_index(current_file_contents, partial_original_code)
                if match_line_index == -1:
                    return partial_original_code
                actual_line = current_file_contents.splitlines()[match_line_index]
                if partial_original_code != actual_line:
                    temp_partial_original_code = actual_line
                    self.current_response = reset_rightmost_string(
                        self.current_response,
                        partial_original_code,
                        temp_partial_original_code,
                    )
                    partial_original_code = temp_partial_original_code
        else:  # multiline match
            match_line_index, spaces_needed = find_match_with_leading_spaces(
                current_file_contents, partial_original_code
            )
        if spaces_needed > 0:
            # we need to add spaces to the original code
            temp_partial_original_code = "\n".join(
                " " * spaces_needed + line for line in partial_original_code.splitlines()
            )
            self.current_response = reset_rightmost_string(
                self.current_response, partial_original_code, temp_partial_original_code
            )
            partial_original_code = temp_partial_original_code
        self.current_response = strip_partial_closing_tags(self.current_response)
        partial_original_code = strip_partial_closing_tags(partial_original_code)
        return partial_original_code
    
    def stream(
        self,
        user_message: str,
        request_assistant_message_content: str, # should be set as constant
    ):
        # Main stream loop that handles switching streams when code suggestions are generated
        stream = continuous_llm_calls.stream(
            self.username,
            self.thread,
            content=user_message,
            assistant_message_content=request_assistant_message_content,
            stop_sequences=["</user_response>"],
            model=self.model,
            __version__=STREAM_VERSION,
        )

        result_string = ""
        prefix_string = request_assistant_message_content  # used during stream restarts while generating code suggestions
        while True:
            try:
                current_streamed_text = next(stream)
                if not current_streamed_text:
                    continue
                result_string = prefix_string + current_streamed_text
                yield result_string
                if self.suggested_response:
                    if detect_infinite_loop_in_code_in_suggested_responses(self._all_suggested_responses):
                        raise Exception("Sweep has failed to make code changes. Please report this to support@sweep.dev.")
                    prefix_string, stream = self.consume_suggested_assistant_content()
                    logger.debug(f"Auto-suggested:\n{prefix_string}")
            except StopIteration:
                break


if __name__ == "__main__":
    cloned_repo = MockClonedRepo(
        _repo_dir="/tmp/sweep-internal",
        repo_full_name="sweepai/sweep-internal",
    )
    thread = Thread()
    modify_files_dict = FileModificationState()
    code_change_stream_state: CodeChangeStreamState = CodeChangeStreamState(
        username="test",
        model=LATEST_CLAUDE_MODEL,
        cloned_repo=cloned_repo,
        thread=thread,
        stop_sequences=[],
        modify_files_dict=modify_files_dict,
    )
    test_response = """
<code_change>
<file_path>
tests/utils/test_str_utils.py
</file_path>
<justification>
test
</justification>
<original_code>
```
if __name__ == "__main__":
    pytest.main([__file__])"""

    test_response_truncate = """
<code_change>
<file_path>
tests/utils/test_str_utils.py
</file_path>
<justification>
test
</justification>
<original_code>
```
import pytest
from typing import Iterable, Union
# rest of the code
"""
    # code_change_stream_state.update_state_with_new_response(test_response)
    code_change_stream_state.update_state_with_new_response(test_response_truncate)
    # bp()
