# IMPORTANT: to use the function decorator your function must have the username as the first param
import time
import traceback
from functools import wraps
from typing import Callable, TypeVar

from sweepai.o11y.event_logger import posthog
from sweepai.o11y.telemetry_utils import make_serializable_dict
from sweepai.utils.str_utils import get_hash
from sweepai.utils.streamable_functions import StreamableFunction

T = TypeVar("T")


def posthog_trace(
    function: Callable[..., T],
) -> Callable[..., T]:
    """
    Automatically posthog traces a function\n
    Requires username as the first parameter
    """
    if isinstance(function, StreamableFunction):
        raise ValueError(
            "posthog_trace cannot be used on a StreamableFunction, place @streamable before @posthog_trace"
        )

    @wraps(function)
    def wrapper(username: str, *args, metadata: dict = {}, **kwargs):
        tracking_id = get_hash()[:10]
        metadata = {**metadata, "tracking_id": tracking_id, "username": username}
        # attach args and kwargs to metadata
        if args:
            args_names = function.__code__.co_varnames[: function.__code__.co_argcount]
            args_dict = dict(zip(args_names[1:], args))  # skip first arg which must be username
            posthog_args: dict = make_serializable_dict(args_dict)
            metadata = {**metadata, **posthog_args}
        if kwargs:
            posthog_kwargs = make_serializable_dict(kwargs)
            if "access_token" in posthog_kwargs:
                del posthog_kwargs["access_token"]
            metadata = {**metadata, **posthog_kwargs}
        metadata = make_serializable_dict(metadata)
        posthog.capture(username, f"{function.__name__} start", properties=metadata)

        start_time = time.time()

        try:
            # check if metadata is in the function signature
            if "metadata" in function.__code__.co_varnames[: function.__code__.co_argcount]:
                result = function(username, *args, **kwargs, metadata=metadata)
            else:
                result = function(
                    username,
                    *args,
                    **kwargs,
                )
        except Exception as e:
            posthog.capture(
                username,
                f"{function.__name__} error",
                properties={
                    "error": str(e),
                    "trace": traceback.format_exc(),
                    "execution_time": time.time() - start_time,
                    **metadata,
                },
            )
            raise e
        else:
            posthog.capture(
                username,
                f"{function.__name__} success",
                properties={"execution_time": time.time() - start_time, **metadata},
            )
            return result

    return wrapper
