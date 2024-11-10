"""
List of common prompts used across the codebase.
"""

fix_files_to_change_prompt = """You proposed a plan. However, your proposed plan has the following errors:

<errors>
{error_message}
</errors>

You must resolve these errors before proceeding. Respond in the following format:

<error_resolutions>
<error_resolution>
Error #0: Summary of the error

You will first think step-by-step about the error, and then either rewrite the instructions with the corrected fix, or drop the task.

<thinking>
Analyze extremely carefully in great detail what went wrong, including the file path and the specific code block that needs to be modified. 
If you have failed to copy code verbatim, describe precisely what is different between the code you provided and the code in the actual file. Reference the exact lines in the diff provided showing the difference between your original code and what is in the file.
</thinking>

Then, let's resolve the errors in your proposed plan. You MUST pick ONE of the following options:
a. If you would like to patch the corresponding task of the plan, create a modify block with an index. The index should be equivalent to the error number of this error_resolution block, so it must be one of the following allowed integers: {allowed_indices}.
b. If the error is a file path, correct the file path. This is preferred if the code does not need to be changed.
c. Otherwise, if you absolutely cannot resolve the error, drop the task. 

You must pick exactly ONE option from the three options presented above. Follow this format:

Option a: To patch an invalid modify:

<modify file="file_path" index="0">
Rewritten instructions to resolve the error. Update the original_code and new_code blocks as required, ensuring that the <original_code> block contains the actual code from the file.

Update <original_code> with the necessary changes:
<original_code>
The corrected code from the file verbatim. Abbreviating, missing indents, paraphrasing and placeholder code are NOT permitted. It is absolutely critical that the indentation is correct and matches the source code EXACTLY.
</original_code>

Update <new_code> block with the necessary changes:
<new_code>
Updated new code, based on the corrections in <original_code>. Ensure all newly introduced indents and comments are propagated here.
</new_code>
</modify>

Option b: To fix an invalid file path, such as a non-existent directory (this is preferred if the code does not need to be changed):

Enter "COPIED_FROM_PREVIOUS_MODIFY" verbatim into the modify block to copy the code from the previous change.
Example:
<modify file="file_path" index="0">
COPIED_FROM_PREVIOUS_MODIFY
</modify>

Option c: Otherwise, if you absolutely cannot resolve the error, drop the task like so:

<drop>Index of the task to drop</drop>
</error_resolution>

[additional <error_resolution> blocks as needed, for the same file or different files]
</error_resolutions>"""

gha_files_to_change_system_prompt = """You are an AI assistant for analyzing failing errors in a developer's code. You will be provided code files, a description of the issue, the error log, relevant parts of the codebase, and the changes he's made.

Your role is to analyze the issue and codebase. Reference specific files, functions, variables and code files in your analysis.

Take these steps:
1. Analyze the issue, codebase and existing changes to understand the problem.

2. List ALL new errors that have appeared in the GitHub Action logs and their corresponding root causes. Identify ALL the entities that need to be updated to resolve these errors. You are diligent and won't miss any errors or entities."""

gha_files_to_change_system_prompt_2 = """You are an AI assistant for writing code to fix failing errors in a developer's code. You will be provided code files, a description of the issue, the error log, relevant parts of the codebase, and the changes he's made. You may only modify edit files to resolve the issue.

Your role is to analyze the issue and codebase, then write out code changes to fix the errors using the proposed diff format. Reference specific files, functions, variables and code files in your plan.
Prioritize using existing code and functions to make efficient and maintainable changes. Ensure your suggestions fully resolve the issue.

Take these steps:
Create a set of code to remove and code to add, including all necessary changes to resolve the issue, in the following format:
Step 1. Reference the original code in <original_code> tags, copying them VERBATIM from the file, with correct indentation and whitespace.
    - Do NOT paraphrase or abbreviate the source code.
    - Placeholder comments like "# existing code" are not permitted.
    - Start with the closest header several lines before the target code and end with the closest end of the block or several lines after the code.
Step 2. Write the new code in <new_code> tags, specifying necessary imports and including relevant type definitions, interfaces, and schemas.
    - BE EXACT as this code will replace the mentioned <original_code>.
Step 3. Look carefully to find all similar changes (potentially unreported) in the code that need to be made in other parts of the same file. Address those as well."""

gha_files_to_change_prompt = """Your job is to analyze the provided issue, error log, relevant parts of the codebase, and changes he's made to understand the requested change.

Follow the following XML format:

# 1. Thinking:
<thinking>
a. Summarize what the original GitHub issue is and asks us to do.

b. List ALL the changes made so far in extreme detail. Be absolutely complete. Follow this format:
    - File path 1:
        - Description of first diff hunk in extreme detail.
        - Description of second diff hunk in extreme detail.
        [additional changes as needed]
    - File path 2:
        - Description of first diff hunk in extreme detail.
        - Description of second diff hunk in extreme detail.
        [additional changes as needed]
    [additional files as needed]
</thinking>

# 2. Reflect:
<reflection>
a. List out all the previous error logs that were solved.
b. List out all previous error logs that are still present or only partially solved.
c. Identify the number of errors, and list out the indices of all the new Github Action error logs that you must now solve and potential root causes and solutions.
- Error 1/n: For each error answer the following questions:
    1. What is the error message? Repeat it verbatim. Is this a repeat error? If so, you may skip the rest of the questions and simply reference the first appearance of this error.
    2. What is the root cause of the error? Explain why.
    3. How can we resolve the error? Be complete and precise.
    4. If we make the fix, what are the potential side effects? Will the fix break other parts of the code? For example, if we change a function signature, will we need to update all the calls to that function?
    5. If you identify potential side effects create - Side Effect #n block and describe the changes that need to be made in order to fix the side effect.
[repeat for all errors]
</reflection>"""

gha_files_to_change_prompt_2 = """Now that you've analyzed the issue and error logs, your job is to write code changes to help resolve the errors in his code while also resolving the GitHub issue.
For each unique error log identified in the previous step, you will need to provide a set of code changes to fix the error.

Guidelines:
<guidelines>
- Always include the full file path and reference the provided files 
- Prioritize using existing code and utility methods to minimize writing new code
- Break the task into small steps, with each <modify> section for each logical code block worth of change. Use multiple <modify> blocks for the same file if there are multiple distinct changes to make in that file, such as for imports.
- A <modify> block must contain exactly one change in one <new_code> tag.
- To remove code, replace it with empty <new_code> tags.
- Do not make a change that has already been made by the developer.
<guidelines>

Please use the following XML format for your response:

<plan>
There are a total of n errors. List ALL the types of error messages in the current error logs and their root causes. Follow this format:

<error_analysis index="1">
Error message 1/n: Identify the error message.
1. Then, find all lines of code that may have the same failure as the erroring lines of code.
2. Identify the root cause of the error, i.e. whether the error is due to a missing change in the tests or the source code. Most of the time, the test case has yet to be updated.
3. Explain how to resolve the error in the test case. Be complete and precise. Remember that to resolve the error in a way such that the test case is still valid. Do not simply apply a band-aid solution to make the error go away.
4. Look carefully to find all similar changes (potentially unreported) in the code that need to be made in other parts of the same file. Address those as well.

Then, based on the analysis, propose a fix by following the format below. If the error has already been fixed, you can skip this step.

<modify file="file_path"> 
Instructions for modifying one section of the file. Each block must have exactly one original_code and one new_code block.

a. Describe the section of code that needs to be modified.
<original_code>
Copy the original_code here VERBATIM from the file.
Do NOT paraphrase or abbreviate the source code.
Placeholder comments like "# existing code" are not permitted.
Start a few lines before the target code to change and end a few lines after.
Do not edit the same area of code more than once to avoid merge conflicts with other modifies.
</original_code>

b. Describe the changes that need to be made to the code.
<new_code>
Write the new code in <new_code> tags, specifying necessary imports and referencing relevant type definitions, interfaces, and schemas. BE EXACT as this code will replace the mentioned <original_code>. This code MUST be different from the original_code.
</new_code>

Use multiple <modify> blocks for the same file to separate distinct changes, such as for imports.
</modify>

Then, determine if there are similar issues that we should also resolve. Make as many additional modify blocks as needed until ALL similar issues are resolved.
Any issue that doesn't have a corresponding modify block will not be fixed, you must make modify blocks for every single issue identified.
Do not attempt to fix multiple issues with a single modify block, each issue must have its own modify block.
</error_analysis>
[additional <error_analysis> blocks as needed, for ALL error messages in the error logs
</plan>"""

plan_selection_prompt = """Critique the pros and cons of each plan based on the following guidelines, prioritizing thoroughness and correctness over potential performance overhead: 
- Correctness: The code change should fully address the original issue or requirement without introducing new bugs, security vulnerabilities, or performance problems. Follow defensive programming practices, such as avoiding implicit assumptions, validating inputs, and handling edge cases. Consider the potential impact on all relevant data structures and ensure the solution maintains data integrity and consistency. Thoroughness is a top priority. 
- Backwards Compatibility: When possible, avoid breaking changes to public APIs, data formats, or behaviors that existing code depends on. 
- Clarity: The code change should be readable, well-structured, and easy for other developers to understand and maintain. Follow existing conventions and style guides, and include documentation and comments for complex or non-obvious logic. 
- Simplicity: Strive for a solution that is as simple as possible while still being complete and correct. Favor straightforward and easily understandable code. Performance overhead should not be a factor in evaluating simplicity. 
- Integration: Assess how well the change fits with the overall architecture and design of the system. Avoid tightly coupling components or introducing new dependencies that could complicate future development or deployment. After evaluating the plans against these criteria, select the one that provides the most thorough and correct solution within the specific context and constraints of the project. Prioritize long-term maintainability and architectural integrity.

Respond using the following XML format:

<final_plan>
[Insert the final plan here, including any modifications or improvements based on the feedback and dialogue. Explain how the plan aligns with the guidelines and why it was chosen over the alternatives.]
</final_plan>

Here is an example response format:

<final_plan>
<modify file="example.py">
[Example instructions here]
</modify>
...
<modify file="anotherexamplefile.py">
[More example instructions here]
</modify>
[Your explanation of why this plan was chosen and how it aligns with the guidelines and any modications made to this plan]
</final_plan>"""
