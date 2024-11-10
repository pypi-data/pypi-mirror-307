def merge_snippet_ranges(ranges: list[tuple[int, int]], context_lines: int = 0) -> list[tuple[int, int]]:
    """
    Merges overlapping ranges and ranges within context_lines of each other
    """
    if not ranges:
        return []
    ranges.sort(key=lambda x: x[0])
    merged_ranges = [ranges[0]]
    for current_start, current_end in ranges[1:]:
        previous_start, previous_end = merged_ranges[-1]
        # Check if the current range is within context_lines of the previous range
        if current_start <= previous_end + context_lines:
            merged_ranges[-1] = (previous_start, max(previous_end, current_end))
        else:
            merged_ranges.append((current_start, current_end))
    return merged_ranges
