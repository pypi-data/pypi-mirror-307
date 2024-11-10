import re
from collections import defaultdict

from loguru import logger

from sweepai.core.github_utils import ClonedRepo

gha_context_cleanup_system_prompt = """You are a skilled programmer. You will be given a set of failing GitHub Action logs. Your sole task is to extract and return only the crucial parts that will help a developer resolve the issues. 
Eliminate any unnecessary context and return verbatim the useful lines of logs."""

gha_generate_query_system_prompt = """You are a skilled programmer. You will be given a set of failing GitHub Action logs. 
Your sole task is to create a query based on the failing Github Action logs that will be used to vector search a code base in order to fetch relevant code snippets.
The retrived code snippets will then be used as context to help the next developer resolve the failing Github Action logs."""

gha_context_cleanup_user_prompt = """
# The failing Github Action logs are given below

{github_actions_logs}

ONLY RETURN THE USEFUL PARTS OF THE LOGS THAT WILL HELP A DEVELOPER RESOLVE THE ISSUES. NOTHING ELSE.
"""

gha_generate_query_user_prompt = """
# The failing Github Action logs are given below

{github_actions_logs}

# The initial task that resulted in these failing Github Action logs is given below

{issue_description}

Return your query below in the following xml tags:
<query>
{{generated query goes here. Remember that it will be used in a vector search so tailor your query with that in mind. There will not be multiple searches, this one search needs to get all the revelant code snippets for all issues}}
</query>
"""

SLEEP_DURATION_SECONDS = 5


def get_error_locations_from_error_logs(error_logs: str, cloned_repo: ClonedRepo):
    pattern = re.compile(
        r"^(?P<file_path>.*?)[^a-zA-Z\d]+(?P<line_num>\d+)[^a-zA-Z\d]+(?P<col_num>\d+)[^a-zA-Z\d]+(?P<error_message>.*?)$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(error_logs))

    matched_files = []
    errors = defaultdict(dict)
    error_message = ""
    try:
        file_paths = cloned_repo.get_file_list()
        for match in matches:
            potential_file_path = match.group("file_path")
            line_number = match.group("line_num")
            current_error_message = match.group("error_message")
            if not any(file_path in potential_file_path for file_path in file_paths):
                # include raw message if we cannot find the file
                error_message += f"{match.group(0)}\n"
                continue
            actual_file_path = [file_path for file_path in file_paths if file_path in potential_file_path][0]
            matched_files.append(actual_file_path)

            errors[actual_file_path][int(line_number)] = current_error_message  # assume one error per line for now

        for file_path, errors_dict in errors.items():
            error_message += f"Here are the {len(errors_dict)} errors in {file_path}, each denotated by FIXME:\n```\n"
            file_contents = cloned_repo.get_file_contents(file_path)
            lines = file_contents.splitlines()
            erroring_lines = set()
            surrounding_lines = 5
            for line_number in errors_dict.keys():
                erroring_lines |= set(range(line_number - surrounding_lines, line_number + surrounding_lines))
            erroring_lines &= set(range(len(lines)))
            width = len(str(len(lines)))
            for i in sorted(list(erroring_lines)):
                if i not in erroring_lines:
                    error_message += "...\n"
                error_message += str(i + 1).ljust(width) + f" | {lines[i + 1]}"
                if i + 1 in errors_dict:
                    error_message += f"     FIXME {errors_dict[i + 1].strip()}"
                error_message += "\n"
            if len(lines) not in erroring_lines:
                error_message += "...\n"
            error_message += "```\n"
        deduped_matched_files = []
        for file_path in matched_files:
            if file_path not in deduped_matched_files:
                deduped_matched_files.append(file_path)
        if (
            not error_message
        ):  # monkey patch because this can fail and return empty error_message, which is not what we want
            return error_logs, []
        return error_message, deduped_matched_files
    except Exception as e:
        logger.error(f"Error in getting error locations: {e}")
        return error_logs, []
