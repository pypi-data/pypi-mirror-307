# Source: https://gist.github.com/TACIXAT/c5b2db4a80c812c4b4373b65e179a220
"""Formats an sexpression for pretty printing."""


def format_sexpression(s, indent_level=0, indent_size=2):
    """ChatGPT + TACIXAT"""
    output = ""
    i = 0
    # Initialize to False to avoid newline for the first token
    need_newline = False
    cdepth = []  # Track colons
    while i < len(s):
        if s[i] == "(":
            output += "\n" + " " * (indent_level * indent_size) + "("
            indent_level += 1
            need_newline = False  # Avoid newline after opening parenthesis
        elif s[i] == ":":
            indent_level += 1
            cdepth.append(indent_level)  # Store depth where we saw colon
            output += ":"
        elif s[i] == ")":
            indent_level -= 1
            if len(cdepth) > 0 and indent_level == cdepth[-1]:
                # Unindent when we return to the depth we saw the last colon
                cdepth.pop()
                indent_level -= 1
            output += ")"
            need_newline = True  # Newline needed after closing parenthesis
        elif s[i] == " ":
            output += " "
        else:
            j = i
            while j < len(s) and s[j] not in ["(", ")", " ", ":"]:
                j += 1
            # Add newline and indentation only when needed
            if need_newline:
                output += "\n" + " " * (indent_level * indent_size)
            output += s[i:j]
            i = j - 1
            need_newline = True  # Next token should start on a new line
        i += 1
    return output
