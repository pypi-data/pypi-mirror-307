from loguru import logger
from sweepai.core.github_utils import ClonedRepo, temporary_cloned_repo_copy
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.modify.validate.code_validators import format_file
from sweepai.utils.diff import generate_diff


def format_changes(
    modify_files_dict: FileModificationState,
    cloned_repo: ClonedRepo,
):
    with temporary_cloned_repo_copy(cloned_repo) as temp_repo:
        for file_path, file_contents in modify_files_dict.files.items():
            formatted_original_contents = format_file(file_path, file_contents.original_contents, temp_repo.repo_dir)
            lines_diff_from_original = generate_diff(formatted_original_contents, file_contents.original_contents).count("\n")

            min_diff_size_to_format = 0.3 * len(formatted_original_contents.split("\n"))
            if lines_diff_from_original <= max(25, min_diff_size_to_format): # less than 25 lines or 30% of the file
                file_contents.new_contents = format_file(file_path, file_contents.new_contents, temp_repo.repo_dir)
            else:
                logger.warning(f"File {file_path} was not formatted, {lines_diff_from_original} lines different from original")
    return modify_files_dict

