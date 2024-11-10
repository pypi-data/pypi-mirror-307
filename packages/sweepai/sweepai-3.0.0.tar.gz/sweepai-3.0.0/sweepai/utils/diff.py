import difflib


def generate_diff(old_code: str, new_code: str, **kwargs):
    if old_code == new_code:
        return ""
    stripped_old_code = old_code.strip("\n") + "\n"
    stripped_new_code = new_code.strip("\n") + "\n"

    # Split the code into lines, preserving the line endings
    old_lines = old_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)

    # Add a newline character at the end if it's missing
    if not old_code.endswith("\n"):
        old_lines.append("\n")
    if not new_code.endswith("\n"):
        new_lines.append("\n")

    default_kwargs = {"n": 5}
    default_kwargs.update(kwargs)

    diff = difflib.unified_diff(
        stripped_old_code.splitlines(keepends=True), stripped_new_code.splitlines(keepends=True), **kwargs
    )

    diff_result = ""

    for line in diff:
        if not line.endswith("\n"):
            line += "\n"
        diff_result += line

    return diff_result


def generate_diff_statistics(original_code: str, new_code: str) -> str:
    diff = generate_diff(original_code, new_code)
    return diff.count("\n+"), diff.count("\n-")


def remove_whitespace_changes(patch: str) -> str:
    lines = patch.split("\n")
    result = []
    in_hunk = False
    hunk_lines = []
    hunk_header = None

    for line in lines:
        if line.startswith("@@"):
            if in_hunk:
                processed_hunk = process_hunk(hunk_header, hunk_lines)
                if processed_hunk:
                    result.extend(processed_hunk)
            hunk_header = line
            hunk_lines = []
            in_hunk = True
        elif in_hunk:
            hunk_lines.append(line)
        else:
            result.append(line)

    if in_hunk:
        processed_hunk = process_hunk(hunk_header, hunk_lines)
        if processed_hunk:
            result.extend(processed_hunk)

    return "\n".join(filter(None, result))


def should_skip_line(current_line: str, next_line: str) -> bool:
    """This assumes that diffs are ordered in a way that +/- lines are next to each other and - comes before +."""
    if not next_line.startswith("+"):
        return False
    # check if current_line is equal to next_line if both right sides are stripped (don't lstrip because python indentation matters)
    return current_line[1:].rstrip() == next_line[1:].rstrip()


def process_hunk(header: str, hunk: list[str]) -> list[str]:
    processed = []
    changes: list[str] = []
    context_buffer = []

    def flush_changes():
        nonlocal processed, changes, context_buffer
        if changes:
            # Process changes to remove pairs of whitespace-only +/- lines
            cleaned_changes = []
            i = 0
            while i < len(changes):
                line = changes[i]
                if line.startswith("-"):
                    # check if next line is a pure whitespace diff
                    if i + 1 < len(changes):
                        next_line = changes[i + 1]
                        if should_skip_line(current_line=line, next_line=next_line):
                            # Skip both lines
                            i += 2
                            continue
                cleaned_changes.append(line)
                i += 1
            changes = cleaned_changes

            if changes:
                # Check if all remaining changes are whitespace-only
                if all(line[1:].strip() == "" for line in changes):
                    changes = []  # Discard all whitespace-only changes
                else:
                    processed.extend(context_buffer)
                    processed.extend(changes)
            context_buffer = []
            changes = []

    for line in hunk:
        if line.startswith("+") or line.startswith("-"):
            changes.append(line)
        else:
            if changes:
                flush_changes()
            context_buffer.append(line)
            if len(context_buffer) > 3:
                processed.append(context_buffer.pop(0))

    flush_changes()

    if processed:
        return [header] + processed
    else:
        return []
