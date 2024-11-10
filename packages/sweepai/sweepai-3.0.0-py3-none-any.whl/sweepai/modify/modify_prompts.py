ORIGINAL_CODE_NOT_PRESENT_BEST_MATCH_PROMPT = """
The original_code provided does not appear to be present in file {file_name}. Your provided original_code contains:\n```\n{original_code}\n```\nDid you mean the following existing code?\n```\n{best_match}\n```\nHere is the difference between the original_code you provided and the most similar existing code from the file, along with its surrounding code:\n```\n{best_match_diff}\n```
"""


DID_YOU_MEAN_PROMPT = """Fix your make_change function call by following these steps:

# 1. Thinking
<thinking>
Describe in great detail how your original_code block differs from what's in the codebase. Are you missing any indentation?
</thinking>

# 2. Function call
Make the make_change function call again, this time ensuring that the original_code parameter matches the code from file.
"""

ORIGINAL_CODE_NOT_FOUND_PROMPT = """The original_code provided does not appear to be present in file {file_path}. Your provided original_code erroneously contains:
```
{original_code}
```

Let's fix this error by responding in the following format. Fill everything in square brackets with the actual contents.

# Thinking
<thinking>
1. List function headers in this file that are relevant to the code we are trying to append, and explain what they each do. For example, if our code is tests multiplication, focus on tests that test multiplication. Follow this format:
    - Function: [function_name] - [description]
    [additional functions]
Based on these options, deterimine the most similar function header to the original_code you provided.

2. Now, copy JUST THE FIRST OR LAST TEN LINES of the ACTUAL contents of {file_path} to the previous <original_code>. This will go into the <original_code> parameter of the new function call. Follow this format:
```
[JUST FIRST OR LAST TEN LINES of the ACTUAL contents of {file_path}]
```
</thinking>

# Function call
Then, follow up with a make_change function call with the corrected parameters. If you are unable to find the correct section of code, call the submit_task function with an explanation of the issue."""

MULTIPLE_OCCURRENCES_PROMPT = """You MUST resolve this error by following these steps:

# 1. Thinking
<thinking>
a. Identify whether you want to replace all occurrences of the original code or only a specific one. If you want to replace all occurrences, you can use the replace_all flag by adding <replace_all>true</replace_all> to the function arguments.
b. If you want to replace only a specific occurrence, which occurrence you want to replace and the corresponding surrounding context, following this format:

Corrected original code:
```
The original_code block you want to replace with surrounding context.
```

Corrected new code:
```
The new_code block you want to replace with the same surrounding context.
```
</thinking>

# 2. Function Call
Then, call the make_change function again with either the replace_all flag or additional context in the original_code block to specify which occurrence you want to replace."""

LINTER_WARNING_PROMPT = """There is a linter warning in the code changes. Resolve the warnings by following this format:

# Thinking
<thinking>
a. Look closely at the changes made and critique the change(s) you have made for any potential logical errors.
b. Identify what the linter warning is, and what may be causing it. Keep in mind that the actual cause of the error may be different from what the linter is suggesting, such as inconsistent indentation.
c. Indicate the minimum amount of changes required to resolve the linter warnings.
d. Say "I will not be lazy and include all lines of code in the original and new code blocks I create"
</thinking>

Then, call the make_change function to fix the linter warnings. If the warning absolutely cannot or should not be resolved, call submit_task with an explanation of the issue."""

LINTER_INDENTATION_WARNING_PROMPT = """There is a linter warning in the code changes. It also looks like you have changed the indentation of the code, which may be the cause of the error.

Resolve the warnings by following this format:

# Thinking
<thinking>
a. Look closely at the changes made to identify any syntax errors that may have caused the linter errors. Does the number of indents in the changed code compare to the number of indents in the surrounding code?
b. Critique the change(s) you have made for any potential logical errors.
c. Identify what the linter warning is, and what may be causing it. Keep in mind that the actual cause of the error may be different from what the linter is suggesting, such as inconsistent indentation.
d. Indicate the minimum amount of changes required to resolve the linter warnings.
e. Say "I will not be lazy and include all lines of code in the original and new code blocks I create"
</thinking>

Then, call the make_change function to fix the linter warnings. If the warning absolutely cannot or should not be resolved, call submit_task with an explanation of the issue."""
