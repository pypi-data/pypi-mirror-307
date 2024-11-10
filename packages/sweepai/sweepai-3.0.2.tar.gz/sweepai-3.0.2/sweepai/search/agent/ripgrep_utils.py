from sweepai.config.client import SweepConfig


def cleaned_rg_output(root_directory: str, sweep_config: SweepConfig, output: str):
    # this function now expects that you ran with the cwd as the root dir for the purposes of file paths
    output = output.replace(f"\n{root_directory}/", "\n")
    result_dict = {}
    for block in output.split("\n\n"):
        if not block.strip():
            continue
        file_path, *contents = block.split("\n")
        if not file_path:
            continue
        if sweep_config.is_file_excluded_aggressive(root_directory, file_path):
            continue
        result_dict[file_path] = "\n".join(contents)
    # serialize contents with a string return type
    result = "\n\n".join([f"{file_path}\n{contents}" for file_path, contents in result_dict.items()])
    return result


# try and find code_snippet inside file_contents given various levels of indentation, and right strip the lines of code
# if successful returns the num of spaces required to find the code match and if we need to rstrip the old code or not
def manual_code_check(file_contents: str, code_snippet: str) -> tuple[int, bool]:
    code_lines = [line for line in code_snippet.split("\n")]
    # special case for single line
    if len(code_lines) == 1:
        file_lines = file_contents.split("\n")
        # check directly
        new_code = code_lines[0]
        # only continue if it is unique, this will then later fail the uniqueness check
        if file_contents.count(new_code) > 1:
            return 0, False
        if new_code in file_contents:
            # now check how many leading whitespaces there are
            for line in file_lines:
                if new_code in line:
                    # unless the code is at the start of the line
                    if line.startswith(new_code):
                        return 0, False
                    return len(line) - len(line.lstrip()), False
        else:
            # now try rstrip if initially the code is not there
            new_code = new_code.rstrip()
            if file_contents.count(new_code) > 1:  # uniqueness check
                return 0, False
            if new_code in file_contents:
                # now check how many leading whitespaces there are
                for line in file_lines:
                    if new_code in line:
                        # unless the code is at the start of the line
                        if line.startswith(new_code):
                            return 0, True
                        return len(line) - len(line.lstrip()), True
        return -1, False

    # assume one indent is two spaces and check max 10 indents
    for indent in range(0, 40, 2):
        new_code_lines = [f"{' ' * indent}{line}" if line.strip() else "" for line in code_lines]
        new_code = "\n".join(new_code_lines)
        if new_code in file_contents:
            return indent, False
    # sometimes llm returns code with trailing whitespace, if we have reached here check again but strip all trailing whitespace
    code_lines = [line.rstrip() for line in code_snippet.split("\n")]
    for indent in range(0, 40, 2):
        new_code_lines = [f"{' ' * indent}{line}" if line.strip() else "" for line in code_lines]
        new_code = "\n".join(new_code_lines)
        if new_code in file_contents:
            return indent, True
    return -1, False
