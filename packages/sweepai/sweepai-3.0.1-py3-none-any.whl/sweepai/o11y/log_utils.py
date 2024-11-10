import contextlib
from datetime import datetime
import os
from contextlib import contextmanager

from loguru import logger

from sweepai.config.server import CACHE_DIRECTORY

LOG_DIRECTORY = f"{CACHE_DIRECTORY}/logs"
os.makedirs(LOG_DIRECTORY, exist_ok=True)


@contextmanager
def log_to_file(tracking_id: str | None):
    # filter_func makes this thread-safe
    if tracking_id:
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(LOG_DIRECTORY, date_str,f"{tracking_id}.log")
        logger.debug(f"Logging to file: {log_file}")

        file_handler = logger.add(
            log_file,
            filter=lambda record: record["extra"].get("tracking_id") == tracking_id,
        )

        with logger.contextualize(tracking_id=tracking_id):
            try:
                yield
            except Exception as e:
                logger.exception(e)
                raise
            else:
                logger.info("Success!")
            finally:
                logger.remove(file_handler)
    else:
        yield


@contextmanager
def log_warnings_to_file(keywords: list[str] = [], tracking_id: str | None = None):
    if tracking_id:
        date_str = datetime.now().strftime("%Y-%m-%d")
        warnings_file = os.path.join(LOG_DIRECTORY, date_str, f"{tracking_id}.err")
        warnings_handler = logger.add(
            warnings_file,
            level="WARNING",
            format=lambda record: f"{record['time']} | {record['level']} | {record['message']}",
            filter=lambda record: record["extra"].get("tracking_id") == tracking_id
            and (not keywords or any(keyword in record["message"] for keyword in keywords)),
        )

        try:
            with logger.contextualize(tracking_id=tracking_id):
                yield
        finally:
            logger.remove(warnings_handler)
    else:
        yield


@contextmanager
def suppress_with_warning(*exceptions: list[BaseException]):
    try:
        yield
    except Exception as e:
        if any(isinstance(e, exception) for exception in exceptions):
            logger.warning(f"Exception {e} suppressed")
        else:
            raise


@contextlib.contextmanager
def mute():
    # Used to use contextlib.redirect_stdout(os.devnull), but this was not thread safe.
    try:
        logger.disable("sweepai.core.llm.chat")
        logger.disable("sweepai.core.llm.viz_utils")
        yield
    finally:
        logger.enable("sweepai.core.llm.chat")
        logger.enable("sweepai.core.llm.viz_utils")
