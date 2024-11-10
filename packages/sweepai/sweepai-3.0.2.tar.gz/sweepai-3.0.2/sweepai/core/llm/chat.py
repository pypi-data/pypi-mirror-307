import copy
import os
import ssl
import time
from typing import Callable, Iterator, Literal

import backoff
from anthropic import (
    Anthropic,
    AnthropicBedrock,
    APIStatusError,
    InternalServerError,
    RateLimitError,
    Stream,
)
from anthropic.types import MessageStreamEvent
from boto3 import client as boto3_client
from httpx import Client
from loguru import logger
from openai import AzureOpenAI, OpenAI
from pydantic import BaseModel

from sweepai.config.server import (
    AWS_ACCESS_KEY,
    AWS_ANTHROPIC_AVAILABLE,
    AWS_ANTHROPIC_BASE_URL,
    AWS_REGION,
    AWS_SECRET_KEY,
    AZURE_API_KEY,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
    CURL_CA_BUNDLE,
    DEEPSEEK_API_KEY,
    DEFAULT_GPT4_MODEL,
    MISTRAL_API_KEY,
    TOGETHER_API_KEY,
)
from sweepai.core.entities import AssistantMessage, Message, SystemMessage, UserMessage
from sweepai.core.llm.image_utils import create_message_with_images
from sweepai.core.llm.openai_proxy import OpenAIProxy
from sweepai.core.llm.viz_utils import save_messages_for_visualization
from sweepai.utils.cache import create_cache
from sweepai.utils.str_utils import (
    format_json_string,
    truncate_text_based_on_stop_sequence,
)
from sweepai.utils.streamable_functions import cached_streamable, streamable

cache = create_cache()
openai_proxy = OpenAIProxy()

OpenAIModel = Literal[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-08-06",
    "o1-preview",
    "o1-mini",
    "deepseek-coder",
    "meta.llama3-1-8b-instruct-v1:0",
    "meta.llama3-1-70b-instruct-v1:0",
    "meta.llama3-1-405b-instruct-v1:0",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "mistral-large-latest",
]

AnthropicModel = Literal[
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-opus-20240229",
]

ChatModel = OpenAIModel | AnthropicModel

model_to_max_tokens: dict[ChatModel, int] = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-4-1106-preview": 128000,
    "gpt-4-0125-preview": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4o": 128000,
    "gpt-4o-2024-08-06": 128000,
    "gpt-4o-mini-2024-07-18": 128000,
    "claude-v1": 9000,
    "claude-v1.3-100k": 100000,
    "claude-instant-v1.3-100k": 100000,
    "o1-preview": 128000,
    "o1-mini": 128000,
    "anthropic.claude-3-haiku-20240229-v1:0": 200000,
    "anthropic.claude-3-sonnet-20240229-v1:0": 200000,
    "claude-3-opus-20240229": 200000,
    "claude-3-sonnet-20240229": 200000,
    "claude-3-5-sonnet-20240620": 200000,
    "claude-3-5-sonnet-20241022": 200000,
    "claude-3-haiku-20240307": 200000,
    "claude-3-5-haiku-20241022": 200000,
    "gpt-3.5-turbo-16k-0613": 16000,
    "deepseek-coder": 128000,
    "meta.llama3-1-8b-instruct-v1:0": 128000,
    "meta.llama3-1-70b-instruct-v1:0": 128000,
    "meta.llama3-1-405b-instruct-v1:0": 128000,
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": 128000,
    "mistral-large-latest": 128000,
}

default_temperature = 0.1

LATEST_CLAUDE_SONNET_MODEL = "claude-3-5-sonnet-20241022"
LATEST_CLAUDE_MODEL = "claude-3-5-haiku-20241022"

def is_openai_model(model: str) -> bool:
    return model.startswith("deepseek") or model.startswith("o1-") or model.startswith("gpt-4")


def is_rate_limit_or_overloaded_error(e):
    return isinstance(e, (RateLimitError, APIStatusError)) and e.status_code in (
        429,
        500,
        529,
    )


def wrap_anthropic_messages_with_cache(
    message_dicts: list[dict],
    indices: list[int] = [-2, -1, 1, 2],
):
    for index in indices:
        # check if index is in bounds here on both sides
        # the string type check is sufficient to prevent double wrapping
        index_valid = -len(message_dicts) <= index < len(message_dicts)
        if index_valid and isinstance(message_dicts[index]["content"], str):
            message_dicts[index]["content"] = [
                {
                    "type": "text",
                    "text": message_dicts[index]["content"],
                    "cache_control": {"type": "ephemeral"},
                }
            ]
    return message_dicts


# go through each message and see if we need to update it to include images or not
def add_images_to_messages(
    message_dicts: list[dict[str, str]],
    images: list[tuple[str, str, str]],
    use_openai: bool = False,
):
    if not images:
        return message_dicts
    try:
        new_message_dicts = []
        for message in message_dicts:
            new_message = create_message_with_images(message, images, use_openai=use_openai)
            new_message_dicts.append(new_message)
    except Exception as e:
        logger.error(f"Error in adding images to messages: {e}")
        return message_dicts
    return new_message_dicts


class Thread(BaseModel):
    messages: list[Message] = []
    model: ChatModel = DEFAULT_GPT4_MODEL
    file_change_paths: list[str] = []
    temperature: float = default_temperature

    class Config:
        arbitrary_types_allowed = True

    @property
    def messages_dicts(self):
        # Remove the key from the message object before sending to OpenAI
        cleaned_messages = [message.to_openai() for message in self.messages]
        return cleaned_messages

    @property
    def roles(self):
        return [message.role for message in self.messages]

    def __getitem__(self, item):
        return self.messages[item]

    def __iter__(self):
        return iter(self.messages)

    def __next__(self):
        return next(self.messages)

    def __len__(self):
        return len(self.messages)

    @property
    def last(self):
        return self.messages[-1]

    @property
    def anthropic_messages_dicts(self):
        """This method should never set state, only return the current state"""
        # Clean up multiple user messages in a row
        new_messages = []
        for message in self.messages_dicts:
            if message["role"] == "system":
                continue
            is_message_role_the_same = new_messages and new_messages[-1]["role"] == message["role"]
            if is_message_role_the_same:
                # this validates that the new message is not blank
                if message["content"].rstrip():
                    new_messages[-1]["content"] += "\n\n" + message["content"].rstrip()
            else:
                message["content"] = message["content"].rstrip()
                new_messages.append(copy.deepcopy(message))
        # We're seeing 400 errors from anthropic where the message is empty. Fixing this here but also adding a log
        for message in new_messages:
            if not message["content"]:
                message_order_log = [f'{message["role"]}\n{message["content"][:100]}' for message in new_messages]
                logger.error(f"Empty message found: {message}, message roles:\n{message_order_log}")
        # now parse out the empty messages, this may cause ANOTHER error because they aren't alternating, which we'll fix later
        new_messages = [message for message in new_messages if message["content"]]
        return new_messages

    @classmethod
    def from_system_message_string(cls, prompt_string: str, **kwargs):
        return cls(
            messages=[SystemMessage(content=prompt_string)],
            **kwargs,
        )

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RateLimitError, APIStatusError),
        base=10,
        factor=2,
        max_time=40,
        max_tries=3,
        giveup=lambda e: not is_rate_limit_or_overloaded_error(e),
    )
    def chat(
        self,
        content: str,
        assistant_message_content: str = "",
        model: ChatModel = "claude-3-haiku-20240307",
        temperature: float | None = None,
        stop_sequences: list[str] = [],
        max_tokens: int = 4096,
        verbose: bool = True,
        images: list[tuple[str, str, str]] | None = None,
        stream: bool = False,
        __version__: int = 1,
    ) -> str | Iterator[str]:
        use_openai = is_openai_model(model)
        if use_openai:
            OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
            assert OPENAI_API_KEY or AZURE_API_KEY or AZURE_OPENAI_API_KEY
            max_tokens = 4096
            if self.model.startswith("gpt"):
                self.model = "gpt-4o"
            for message in self.messages:  # Not sure why this is needed
                if message.role == "system":
                    message.role = "user"
        else:
            ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
            assert ANTHROPIC_API_KEY
            self.model = model
            if (AWS_ACCESS_KEY and AWS_SECRET_KEY and AWS_REGION) or model != LATEST_CLAUDE_MODEL:
                max_tokens = 4096
        if content:
            self.messages.append(Message(role="user", content=content))
        if assistant_message_content:
            self.messages.append(Message(role="assistant", content=assistant_message_content))
        temperature = temperature or self.temperature or default_temperature
        if verbose:
            # messages_string_to_log = '\n\n'.join([message.content for message in self.messages])
            if use_openai:
                logger.debug(f"Calling openai with model {model}\nInput:\n{content}")
            else:
                logger.debug(f"Calling anthropic with model {model}\nInput:\n{content}")
        system_message = "\n\n".join([message.content for message in self.messages if message.role == "system"])
        content = ""
        e = None
        NUM_ANTHROPIC_RETRIES = 6
        use_aws = True

        def llm_stream():
            nonlocal model
            model = model or self.model
            streamed_text = "" if not assistant_message_content else assistant_message_content
            if use_openai:
                if model.startswith("deepseek"):
                    client = OpenAI(
                        api_key=DEEPSEEK_API_KEY,
                        base_url="https://api.deepseek.com",
                    )
                else:
                    if AZURE_OPENAI_API_KEY and AZURE_OPENAI_API_VERSION and AZURE_OPENAI_ENDPOINT:
                        http_client = None
                        if CURL_CA_BUNDLE:
                            http_client = Client(
                                verify=ssl.create_default_context(cafile=CURL_CA_BUNDLE),
                                proxies={"all://": None},
                            )
                        client = AzureOpenAI(
                            api_key=AZURE_OPENAI_API_KEY,
                            api_version=AZURE_OPENAI_API_VERSION,
                            azure_endpoint=AZURE_OPENAI_ENDPOINT,
                            http_client=http_client,
                        )
                        model = "gpt-4o-2024-05-13"
                    else:
                        client = OpenAI()
                if model.startswith("o1-"):
                    logger.info(f"Using o1 model {model}")
                    response = client.chat.completions.create(
                        model=model,
                        messages=self.messages_dicts,
                    )
                    streamed_text = (
                        response.choices[0].message.content
                        if not assistant_message_content
                        else assistant_message_content + response.choices[0].message.content
                    )
                    save_messages_for_visualization(
                        self.messages_dicts + [{"role": "assistant", "content": streamed_text}],
                        model_name=model,
                    )
                    yield streamed_text
                else:
                    try:
                        # add another one here for streaming because sometimes we end early
                        save_messages_for_visualization(self.messages_dicts, model_name=model)
                    except Exception as e:
                        logger.warning(f"Error saving messages for visualization: {e}")
                    response = client.chat.completions.create(
                        model=model,
                        messages=self.messages_dicts,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        stream=True,
                    )
                    streamed_text = "" if not assistant_message_content else assistant_message_content
                    for chunk in response:
                        if not chunk.choices:
                            continue
                        new_content = chunk.choices[0].delta.content
                        if new_content:
                            streamed_text += new_content
                            yield new_content
                        if chunk.choices[0].finish_reason == "stop":
                            break
                        for stop_sequence in stop_sequences:
                            if stop_sequence in streamed_text:
                                response = truncate_text_based_on_stop_sequence(streamed_text, stop_sequences)
                                try:
                                    save_messages_for_visualization(
                                        self.messages_dicts + [{"role": "assistant", "content": response}],
                                        model_name=model,
                                    )
                                except Exception as e:
                                    logger.warning(f"Error saving messages for visualization: {e}")
                                return
                    if chunk.choices and chunk.choices[0] and chunk.choices[0].finish_reason:
                        logger.debug(f"finish_reason: {chunk.choices[0].finish_reason}")
            elif model.startswith("meta"):
                if TOGETHER_API_KEY:
                    from together import Together

                    client = Together(api_key=TOGETHER_API_KEY)
                    response = client.chat.completions.create(
                        model=model,
                        messages=self.messages_dicts,
                        max_tokens=min(max_tokens, 4097),
                        temperature=temperature,
                        stop=["<|eot_id|>"],
                        stream=True,
                    )
                    streamed_text = "" if not assistant_message_content else assistant_message_content
                    for chunk in response:
                        new_content = chunk.choices[0].delta.content
                        yield new_content

                        if any(stop_sequence in streamed_text for stop_sequence in stop_sequences):
                            return truncate_text_based_on_stop_sequence(streamed_text, stop_sequences)
                    return streamed_text
                else:
                    client = boto3_client(
                        "bedrock-runtime",
                        region_name=AWS_REGION,
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY,
                    )
                    message_dicts = self.anthropic_messages_dicts
                    message_dicts = [
                        {
                            "role": message["role"],
                            "content": [{"text": message["content"]}],
                        }
                        for message in message_dicts
                    ]

                    streaming_response = client.converse_stream(
                        modelId=model,
                        messages=message_dicts,
                        inferenceConfig={
                            "maxTokens": max_tokens,
                            "temperature": temperature,
                        },
                    )

                    streamed_text = "" if not assistant_message_content else assistant_message_content

                    for chunk in streaming_response["stream"]:
                        if "contentBlockDelta" in chunk:
                            text = chunk["contentBlockDelta"]["delta"]["text"]
                            streamed_text += text
                            yield text

                            if any(stop_sequence in streamed_text for stop_sequence in stop_sequences):
                                response = truncate_text_based_on_stop_sequence(streamed_text, stop_sequences)
                                save_messages_for_visualization(
                                    message_dicts + [{"role": "assistant", "content": response}],
                                    model_name=model,
                                )
                                return response
            elif model == "mistral-large-latest":
                from mistralai import Mistral

                client = Mistral(api_key=MISTRAL_API_KEY)

                chat_response = client.chat.stream(
                    model=model,
                    messages=self.messages_dicts,
                )

                streamed_text = "" if not assistant_message_content else assistant_message_content
                if chat_response is not None:
                    for event in chat_response:
                        streamed_text += event.data.choices[0].delta.content
                        yield event.data.choices[0].delta.content
                        if any(stop_sequence in streamed_text for stop_sequence in stop_sequences):
                            return truncate_text_based_on_stop_sequence(streamed_text, stop_sequences)
            else:
                if AWS_ANTHROPIC_AVAILABLE and use_aws:
                    if "anthropic" not in model:
                        if model == "claude-3-5-sonnet-20241022" or model == "claude-3-5-haiku-20241022":
                            model = "claude-3-5-sonnet-20240620" # sonnet v2 is not supported on bedrock
                        model = f"anthropic.{model}-v1:0"
                    if AWS_ANTHROPIC_BASE_URL:
                        request_headers = {"bedrock-key": ANTHROPIC_API_KEY}
                        client = AnthropicBedrock(
                            aws_access_key=AWS_ACCESS_KEY,
                            aws_secret_key=AWS_SECRET_KEY,
                            base_url=AWS_ANTHROPIC_BASE_URL,
                            http_client=Client(
                                verify=ssl.create_default_context(cafile=CURL_CA_BUNDLE),
                                headers=request_headers,
                            ),
                        )
                    else:
                        client = AnthropicBedrock(
                            aws_access_key=AWS_ACCESS_KEY,
                            aws_secret_key=AWS_SECRET_KEY,
                            aws_region=AWS_REGION,
                        )
                else:
                    client = Anthropic(
                        api_key=ANTHROPIC_API_KEY,
                    )
                start_time = time.time()
                message_dicts = self.anthropic_messages_dicts

                start_time = time.time()
                if verbose:
                    logger.info(f"In queue with model {model}...")
                streamed_text = "" if not assistant_message_content else assistant_message_content
                for retry_count in range(NUM_ANTHROPIC_RETRIES):
                    try:
                        if isinstance(client, AnthropicBedrock):
                            response: Stream[MessageStreamEvent] = client.messages.create(
                                model=model,
                                messages=message_dicts,
                                max_tokens=max_tokens,
                                temperature=temperature,
                                system=system_message,
                                stream=True,
                                # extra_headers={
                                #     "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
                                # } if not (ANTHROPIC_AVAILABLE and use_aws) else {}
                            )
                        else:
                            # PROMPT CACHING START
                            # add cache control to the messages (max 4 messages)
                            message_dicts = wrap_anthropic_messages_with_cache(
                                message_dicts,
                                indices=[
                                    -2,
                                    -1,
                                    1,
                                    2,
                                ],  # TODO: this strategy can be improved later by allowing the caller to pass in the indices
                            )
                            response = client.beta.prompt_caching.messages.create(
                                model=model,
                                messages=message_dicts,
                                max_tokens=max_tokens,
                                temperature=temperature,
                                system=system_message,
                                stream=True,
                                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
                            )
                            # PROMPT CACHING END
                        for event in response:
                            match event.type:
                                case "message_start":
                                    cache_read_input_tokens = (
                                        event.message.usage.cache_read_input_tokens
                                        if hasattr(
                                            event.message.usage,
                                            "cache_read_input_tokens",
                                        )
                                        else 0
                                    )
                                    cache_creation_input_tokens = (
                                        event.message.usage.cache_creation_input_tokens
                                        if hasattr(
                                            event.message.usage,
                                            "cache_creation_input_tokens",
                                        )
                                        else 0
                                    )
                                    if verbose:
                                        logger.info(
                                            f"Starting stream with {event.message.usage.input_tokens} input tokens \nCACHE READ: {cache_read_input_tokens} and \nCACHE_WRITE: {cache_creation_input_tokens} with \n{len(message_dicts)} MESSAGES\nin {time.time() - start_time:.2f}s"
                                        )
                                case "content_block_delta":
                                    streamed_text += event.delta.text
                                    yield event.delta.text
                                    if any(stop_sequence in streamed_text for stop_sequence in stop_sequences):
                                        if verbose:
                                            logger.info(f"Stop sequence hit after {time.time() - start_time:.2f}s")
                                        try:
                                            save_messages_for_visualization(
                                                self.anthropic_messages_dicts
                                                + [
                                                    {
                                                        "role": "assistant",
                                                        "content": streamed_text,
                                                    }
                                                ],
                                                model_name=model,
                                            )
                                            self.messages = self.messages + [AssistantMessage(content=streamed_text)]
                                        except Exception as e:
                                            logger.warning(f"Error saving messages for visualization: {e}")
                                        return truncate_text_based_on_stop_sequence(streamed_text, stop_sequences)
                                case "content_block_stop":
                                    logger.info("")
                                    break
                                case "content_block_start":
                                    logger.info(event)
                                case _:
                                    logger.info(event)
                        break
                    except (APIStatusError, ValueError) as e:
                        # TODO: handle bedrock errors, also check for general AWS error
                        if isinstance(e, APIStatusError):
                            error_message = e.message
                        else:
                            error_message = str(e)
                        logger.warning(f"Error in Anthropic streaming response: {error_message}")
                        if retry_count == (NUM_ANTHROPIC_RETRIES - 1):
                            raise Exception(f"Anthropic API error: {error_message}") from e
                        else:
                            logger.warning(
                                f"Retrying Anthropic call (attempt {retry_count + 1}/{NUM_ANTHROPIC_RETRIES - 1})..."
                            )
                            time.sleep(4 * 1.75**retry_count)
                logger.info(f"Streamed {len(streamed_text)} characters in {time.time() - start_time:.2f}s")
            response = streamed_text
            try:
                save_messages_for_visualization(
                    self.anthropic_messages_dicts + [{"role": "assistant", "content": response}],
                    model_name=model,
                )
                self.messages = self.messages + [AssistantMessage(content=streamed_text)]
            except Exception as e:
                logger.warning(f"Error saving messages for visualization: {e}")
            return response

        if stream:
            return llm_stream()
        else:
            streamed_content = ""
            for new_token in llm_stream():
                streamed_content += new_token
            self.messages.append(AssistantMessage(content=streamed_content))
            if verbose:
                logger.debug(f"{model} response: {self.messages[-1].content}")
            try:
                save_messages_for_visualization(messages=self.anthropic_messages_dicts, model_name=model)
            except Exception as e:
                logger.exception(f"Failed to save messages for visualization due to {e}")
            return self.messages[-1].content


def format_string(s: str, params: dict) -> str:
    # Doing this to avoid format raising on missing inputs, raise on key error instead
    for key, value in params.items():
        placeholder = "{" + key + "}"
        if placeholder in s:
            s = s.replace(placeholder, str(value))
        else:
            raise KeyError(f"Key '{key}' not found in the string")
    return s


def call_llm(
    system_prompt: str,
    user_prompt: str,
    params: dict = {},
    *args,
    **kwargs,
):
    thread: Thread = Thread.from_system_message_string(
        prompt_string=system_prompt,
    )

    if params:
        user_prompt = format_string(user_prompt, params)
    return continuous_llm_calls(
        username=kwargs.get("username", "test_user"),
        content=user_prompt,
        thread=thread,
        *args,
        **kwargs,
    )


@cached_streamable(cache=cache)
def call_anthropic_with_word_buffer(thread: Thread, stop_sequences: list[str] = [], verbose: bool = True, **kwargs):
    # Watch out when using this because if it hits the cache, it won't enter the messages array
    response = ""
    yield ""
    for token in thread.chat(stop_sequences=stop_sequences, stream=True, **kwargs):
        if token:
            # yield the response after a certain point
            # I removed word buffer so we never close <new_code> and reopen the next <code_change>.
            response += token
            yield response
            if verbose:
                print(token, end="", flush=True)


@streamable
def call_anthropic_with_word_buffer_with_cache_handling(
    thread: Thread,
    stop_sequences: list[str] = [],
    content: str = "",
    **kwargs,
):
    thread_length = len(thread)
    response = ""
    for response in call_anthropic_with_word_buffer.stream(
        thread, stop_sequences=stop_sequences, content=content, **kwargs
    ):
        yield response
    if len(thread) == thread_length:
        # Simulates side effects when it hits the cache
        thread.messages.append(UserMessage(content=content))
        thread.messages.append(AssistantMessage(content=response))


def collapse_final_assistant_messages(thread: Thread) -> Thread:
    """
    Collapses the final contiguous block of assistant messages into a single message.
    The block ends when either:
    1. A non-assistant message is encountered
    2. The end of the thread is reached
    
    Example:
        [System, Assistant, Assistant, Assistant] -> [System, Assistant]
        [System, Assistant, Assistant, User] -> [System, Assistant, User]
        [System, Assistant, User, Assistant, Assistant] -> [System, Assistant, User, Assistant]
    
    Args:
        thread: Thread object containing a list of messages
        
    Returns:
        Thread with final contiguous assistant messages collapsed
        
    Raises:
        ValueError: If thread has fewer than 2 messages
    """
    messages = thread.messages
    if len(messages) < 2:
        raise ValueError("Thread must have at least 2 messages to collapse final assistant messages")

    # Find the last non-assistant message or start of thread
    last_idx = len(messages) - 1
    while last_idx >= 0 and messages[last_idx].role == "user":
        last_idx -= 1
        
    # No assistant messages to collapse
    if last_idx < 0 or messages[last_idx].role != "assistant":
        return thread
        
    # Find start of contiguous assistant block
    block_start = last_idx
    while block_start > 0 and messages[block_start - 1].role == "assistant":
        block_start -= 1
        
    # If no multi-message block found, return unchanged
    if block_start == last_idx:
        return thread
        
    # Combine content from messages in the contiguous block
    collapsed_content = "".join(
        message.content 
        for message in messages[block_start:last_idx + 1]
    )
    
    # Create new message list:
    # - Everything before the block
    # - Single collapsed assistant message
    # - Any trailing messages after the block
    collapsed_messages = (
        messages[:block_start] + 
        [Message(role="assistant", content=collapsed_content, key="assistant")] +
        messages[last_idx + 1:]
    )
    
    thread.messages = collapsed_messages
    return thread

def stream_backoff(
    stream_factory: Callable[[], Iterator],
    timeouts: list[float],
    exception_types: list[type[Exception] | str] = [Exception],
):
    error = None
    for timeout in timeouts:
        try:
            yield from stream_factory()
            break
        except Exception as e:
            logger.debug(f"Stream crashed due to {e}")
            for exception_type in exception_types:
                is_match = False
                if isinstance(exception_type, str):
                    # handle string case
                    is_match = exception_type in str(e)
                else:
                    # handle exception type case
                    is_match = isinstance(e, exception_type)
                if is_match:
                    error = e
                    break
            else:
                raise e
            logger.exception(f"Stream failed due to {error}")
            time.sleep(timeout)
    if error:
        raise error


def should_continue_calling_llm(
    latest_llm_generated_response: str,
    stop_sequences: list[str],
    num_calls: int,
    max_calls: int,
    max_token_output: int,
    model: str,
) -> bool:
    # stop if any stop sequence is present
    stop_sequence_present = any(token in latest_llm_generated_response for token in stop_sequences)
    if stop_sequence_present:
        return False
    # stop if we've called too many times
    if num_calls >= max_calls:
        return False
    # call it again if we've generated too many tokens without hitting a stop sequence
    # this previously used 80%, but i've seen the 3.5 factor be wrong by as much as 75%
    didnt_hit_max_tokens = len(latest_llm_generated_response) < (3.5 * max_token_output * 0.5)
    if didnt_hit_max_tokens:
        return False
    if model.startswith("o1-"):
        return False
    return True


@streamable
def continuous_llm_calls(
    username,
    thread: Thread,
    *args,
    stop_sequences: list[str] = ["</plan>"],
    MAX_CALLS=10,
    **kwargs,
):
    """
    Continuously call the LLM until the response is finished
    This will modify thread and will append the responses to the messages array as one singular large assistant message
    """
    response = ""
    for _ in range(3):
        for response in stream_backoff(
            lambda: call_anthropic_with_word_buffer_with_cache_handling.stream(
                thread,
                stop_sequences=stop_sequences,
                *args,
                **kwargs,
            ),
            timeouts=[0, 5, 30],
            exception_types=[InternalServerError, "Anthropic API Error"],
        ):
            yield response
        if response.strip():
            break
    else:
        logger.error(f"Failed to get first response {response}, last_message {thread.messages[-1]}")
    # initialize this to the current_response instead of ""
    # otherwise should_continue_calling_llm would immediately break
    next_response = response
    num_calls = 0
    max_token_output = kwargs.get("max_tokens", 4096)
    while should_continue_calling_llm(
        latest_llm_generated_response=next_response,
        stop_sequences=stop_sequences,
        num_calls=num_calls,
        max_calls=MAX_CALLS,
        max_token_output=max_token_output,
        model=kwargs.get("model", LATEST_CLAUDE_MODEL),
    ):
        content = ""
        response = response.rstrip()
        thread.messages[-1].content = response
        # ask for a second response
        try:
            if "content" in kwargs:
                kwargs.pop("content")
            next_response = ""

            for next_response in stream_backoff(
                lambda: call_anthropic_with_word_buffer_with_cache_handling.stream(
                    thread,
                    content=content,
                    stop_sequences=stop_sequences,
                    *args,
                    **kwargs,
                ),
                timeouts=[0, 5, 30],
                exception_types=[InternalServerError, "Anthropic API Error"],
            ):
                yield response + next_response
            thread = collapse_final_assistant_messages(thread)
            # We should break if this is empty because the LLM hasn't generated anything new
            if not next_response.strip():
                break
            # we can simply concatenate the responses
            response += next_response
        except Exception as e:
            logger.error(f"Failed to get second response due to {e}")
        num_calls += 1
    return response


# UNUSED RIGHT NOW - STRUCTURED OUTPUTS
def get_openai_structured_output(
    messages: list[Message],
    response_format: BaseModel,
    model: str = "gpt-4o-2024-08-06",
) -> BaseModel | None:
    """Returns structured output from OpenAI API, or None if the response is refused."""
    messages = [message.to_openai() for message in messages]
    messages_raw = "\n".join([message["content"] for message in messages])
    logger.debug(f"Calling OpenAI with structured output:\n{messages_raw}")

    def call_structured_output(
        model: str,
        messages: list[dict[str, str]],
        response_format: BaseModel,
    ) -> BaseModel:
        openai_client = OpenAI()
        completion = openai_client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format,
        )
        return completion

    completion = call_structured_output(model=model, messages=messages, response_format=response_format)
    logger.debug(f"OpenAI structured output:\n{format_json_string(completion.choices[0].message.parsed.json())}")
    if completion.choices[0].message.refusal:
        logger.error(f"OpenAI refused to generate structured output: {completion.choices[0].message.refusal}")
        return None
    return completion.choices[0].message.parsed
