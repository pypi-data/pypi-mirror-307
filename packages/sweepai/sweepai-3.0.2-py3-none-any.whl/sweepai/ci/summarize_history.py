from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread, continuous_llm_calls
from sweepai.utils.str_utils import safe_extract_xml_tag

system_message = """You are a helpful assistant that summarizes the history of changes you previously made to a GitHub repository in order to fix a GitHub Actions failure."""

user_message_prompt = """<history>
{history}
</history>

<current_failing_error_logs>
{current_failing_error_logs}
</current_failing_error_logs>

For each of the {n} fix attempts, respond in the following format:

<fix_attempts>
<fix_attempt index="i">
<error>
[what was failing, copying relevant error logs]
</error>
<analysis>
[what you were thinking at this point in time]
</analysis>
<fixes>
[what did you change to address the error? highlight relevant code changes that addresses the error]
</fixes>
<conclusion>
[were you successful? otherwise, what did you incorrectly assume and what did you learn from this fix attempt?]
</conclusion>
</fix_attempt>
</fix_attempts>

# Guidelines:
- Be objective and focus on the codebase. Do not make any interpretations about what may be the root cause of the failure.
- Summarize learnings as "A does not do B", not "I incorrectly assumed A does B".
- Do not say "I didn't analyze the implementation thoroughly" or "I need to look at this closer".

Then summarize everything in the following format, writing in first-person:

<summary>
<successful_fixes>
1. [List all the fixes you made that were successful, what it accomplished and why]
2. [Repeat for each fix attempt]
</successful_fixes>
<unsuccessful_fixes>
1. [List all the fix attempts you made that were unsuccessful, the assumptions you made that were incorrect, and what you learned about the codebase. Be specific about what you tried. Focus on the codebase, do not say "I didn't analyze the implementation thoroughly".]
2. [For each unsuccessful assumption, indicate the number of the fix attempt it is associated with.]
</unsuccessful_fixes>
</summary>"""


def summarize_history(username: str, history: str, current_failing_error_logs: str) -> str:
    if not history:
        return ""
    thread = Thread.from_system_message_string(system_message)
    user_message = user_message_prompt.format(
        history=history,
        current_failing_error_logs=current_failing_error_logs,
        n=history.count("<fix_attempt"),
    )
    response = continuous_llm_calls(
        username=username,
        thread=thread,
        content=user_message,
        stop_sequences=["</summary>"],
        model=LATEST_CLAUDE_MODEL,
    )
    return safe_extract_xml_tag(response, "summary")
