import html
import os
import re
from datetime import datetime
from inspect import stack

from loguru import logger
from pytz import timezone

pst_timezone = timezone("US/Pacific")


def wrap_xml_tags_with_details(text: str) -> str:
    def process_tag(match):
        full_tag = match.group(0)
        is_closing = full_tag.startswith("</")

        if is_closing:
            return "</details>"
        else:
            escaped_tag = html.escape(full_tag)
            return f"<details><summary>{escaped_tag}</summary>"

    processed_text = re.sub(r"<[^>]+>", process_tag, text)

    lines = processed_text.split("\n")
    for i, line in enumerate(lines):
        if not (
            line.strip().startswith("<details")
            or line.strip().startswith("</details")
            or line.strip().startswith("<summary")
        ):
            lines[i] = html.escape(line)

    processed_text = "\n".join(lines)

    return processed_text


llm_call_wrappers = ["continuous_llm_calls", "chat"]

common_terms = {
    "module",
    "run",
    "call",
    "main",
    "invoke",
    "wrapper",
    "run_until_complete",
    "run_forever",
    "_run_once",
    "_run",
    "stream",
    "last",
    "continuous_llm_calls",
    "chat",
    "<module>",
    "async_main",
    "stream_backoff",
    "llm_stream",
    "save_messages_for_visualization",
    "call_anthropic_with_word_buffer_with_cache_handling",
    "call_anthropic_with_word_buffer",
}


def save_messages_for_visualization(messages: list[dict], model_name: str):
    current_datetime = datetime.now(pst_timezone)
    current_year_month_day = current_datetime.strftime("%Y_%m_%d")
    current_hour_minute_second = current_datetime.strftime("%H:%M:%S")
    subfolder = f"sweepai_messages/{current_year_month_day}"

    os.makedirs(subfolder, exist_ok=True)

    frames = stack()
    function_names = [frame.function for frame in frames][::-1]
    filtered_function_names = [
        name for name in function_names if name.lower() not in common_terms and not name.startswith("_")
    ]
    file_path = f"{current_hour_minute_second}"
    for i, function_name in enumerate(filtered_function_names):
        if len(file_path) + len(function_name) > 100:
            break
        file_path += f"_{function_name}"

    raw_file = os.path.join(subfolder, f"{file_path}.xml")
    for i in range(1, 1000):
        if not os.path.exists(raw_file):
            break
        else:
            raw_file = os.path.join(subfolder, f"{file_path}_{i}.xml")

    with open(raw_file, "w") as f_raw:
        total_length = 0
        for i, message in enumerate(messages):
            try:
                content_raw = message["content"]
                message_characters = len(content_raw)
                total_length += message_characters
                message_header = f"{model_name} {message['role']} - {message_characters} characters - {total_length} total characters"
                f_raw.write(
                    f"{message_header}\n<{message['role']}_message>\n{content_raw}\n</{message['role']}_message>\n\n"
                )
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                f_raw.write(f"Error in message processing: {e}\nRaw content: {content_raw}\n\n")

    cwd = os.getcwd()
    logger.info(f"MESSAGES SAVED TO {os.path.join(cwd, raw_file)}")
