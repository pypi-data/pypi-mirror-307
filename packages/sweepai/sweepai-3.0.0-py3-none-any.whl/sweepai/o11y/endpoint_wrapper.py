# IMPORTANT: to use the function decorator your function must have the username as the first param
import asyncio
import traceback
from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException, status
from loguru import logger

from sweepai.o11y.event_logger import posthog
from sweepai.o11y.log_utils import log_to_file
from sweepai.utils.str_utils import get_hash


# TODO: clean this up
def endpoint_wrapper(func: Callable[..., Any]):
    """
    Own custom fastapi wrapper to catch exceptions and log them to posthog and raise errors
    """
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_name = func.__name__
            tracking_id = kwargs.get("tracking_id", get_hash())
            username = kwargs.get("username", "")
            repo_name = kwargs.get("repo_name", "")
            file_path = f"chat-{func_name}-{username}-{repo_name}-{tracking_id}"
            with log_to_file(file_path):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except HTTPException as http_exc:
                    # Re-raise HTTPExceptions without modification
                    raise http_exc
                except Exception as e:
                    # Assuming posthog is properly imported and configured
                    posthog.capture(
                        f"{func_name}_endpoint",
                        f"{func_name}_endpoint error",
                        properties={
                            "error": str(e),
                            "traceback": traceback.format_exc(),
                        },
                    )
                    logger.exception(e)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error: {str(e)}",
                    ) from e

        return wrapper
    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            tracking_id = kwargs.get("tracking_id", get_hash())
            username = kwargs.get("username", "")
            repo_name = kwargs.get("repo_name", "").replace("/", "--")
            file_path = f"chat-{func_name}-{username}-{repo_name}-{tracking_id}"
            with log_to_file(file_path):
                try:
                    result = func(*args, **kwargs)
                    return result
                except HTTPException as http_exc:
                    # Re-raise HTTPExceptions without modification
                    raise http_exc
                except Exception as e:
                    # Assuming posthog is properly imported and configured
                    posthog.capture(
                        f"{func_name}_endpoint",
                        f"{func_name}_endpoint error",
                        properties={
                            "error": str(e),
                            "traceback": traceback.format_exc(),
                        },
                    )
                    logger.exception(e)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error: {str(e)}",
                    ) from e

        return wrapper
