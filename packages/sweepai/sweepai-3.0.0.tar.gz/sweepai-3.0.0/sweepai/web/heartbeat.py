import time
from queue import Empty, Queue
from threading import Thread
from typing import Iterator

from fastapi.responses import StreamingResponse

NOT_SET = object()


def StreamingResponseWithHeartbeat(
    stream_response: Iterator,
    heartbeat_interval: float = 3,
    timeout: float = 30 * 60,
    heartbeat_message: str = NOT_SET,
    **kwargs,
):
    return StreamingResponse(
        stream_with_heartbeat(stream_response, heartbeat_interval, timeout, heartbeat_message, **kwargs)
    )


def stream_with_heartbeat(
    iterator: Iterator[str],
    heartbeat_interval: float = 3,
    timeout: float = 30 * 60,
    heartbeat_message: str = NOT_SET,
):
    queue = Queue()

    def push_thread():
        for item in iterator:
            queue.put(item)

    thread = Thread(target=push_thread)
    thread.start()
    start_time = time.time()
    last_item = None
    while thread.is_alive() and time.time() - start_time < timeout:
        try:
            last_item = queue.get(timeout=heartbeat_interval)
            yield last_item
        except Empty:
            if heartbeat_message is not NOT_SET:
                yield heartbeat_message
            else:
                yield last_item
    if not thread.is_alive():
        # Yield the rest of the items
        while not queue.empty():
            last_item = queue.get()
            yield last_item
    thread.join()
