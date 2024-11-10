import inspect
from copy import deepcopy
from typing import Callable, Generator, Generic, ParamSpec, TypeAlias, TypeVar

from diskcache import Cache
from loguru import logger

from sweepai.config.server import DEV
from sweepai.utils.cache import recursive_hash

InputType = ParamSpec("InputType")
YieldType = TypeVar("YieldType")
ReturnType = TypeVar("ReturnType")
UNSET = object()

# TODO: cleaner stream type
# TODO: StreamableResults

CACHE_ENABLED = DEV
CACHE_VERSION = "v0.1"


def last(
    generator: Generator[YieldType, None, ReturnType],
    default: YieldType | ReturnType = None,
) -> YieldType | ReturnType:
    """
    Returns the last yield or return result of the generator
    """
    result: YieldType | ReturnType = default
    try:
        while True:
            result = next(generator)
    except StopIteration as e:
        if e.value is not None:
            result = e.value
    return result


class StreamableFunction(Generic[InputType, ReturnType, YieldType]):
    """
    Streamable functions allow for the streaming of a function's intermediate results.
    This is great because you can call the function normally, and it will return the function's return value,
    or the last yielded value, if the function has no return.
    But you can also call .stream() on the function, and it will return a generator that yields the intermediate results.
    """

    def __init__(
        self,
        stream: Callable[InputType, Generator[YieldType, None, ReturnType]],
        cache: Cache | None = None,
        ignore_params: list[str] = [],
    ):
        self._stream = stream
        self.cache = cache
        self.ignore_params = ignore_params

    def get_cache(self, key):
        if self.cache is not None and CACHE_ENABLED:
            return self.cache.get(key)

    def cache_key(self, *args, **kwargs):
        if self.cache is None or not CACHE_ENABLED:
            return None
        kwargs_ = {k: v for k, v in kwargs.items() if k not in self.ignore_params}
        return recursive_hash((self._stream.__name__, deepcopy(args), deepcopy(kwargs_), CACHE_VERSION))

    def set_cache(self, key, value):
        if self.cache is not None and CACHE_ENABLED:
            self.cache.set(key, value)

    def delete_cache(self, key):
        if self.cache is not None and CACHE_ENABLED:
            self.cache.delete(key)

    def stream(self, *args: InputType.args, **kwargs: InputType.kwargs) -> Generator[YieldType, None, ReturnType]:
        key = self.cache_key(*args, **kwargs)
        # inlining this with the walrus operator causes issues because we set result to a bool
        if result := self.get_cache(key):
            cached_stream, final_result = result
            logger.info("Reading from cached stream")
            yield from cached_stream
            return final_result
        item = UNSET
        stream = self._stream(*args, **kwargs)
        cached_stream = []
        stream_completed = True
        try:
            try:
                while True:
                    item = next(stream)
                    cached_stream.append(item)
                    self.set_cache(key, (cached_stream, item))
                    yield item
            except StopIteration as e:
                if e.value is not None:
                    item = e.value
                stream_completed = False
            if item is UNSET:
                if DEV:
                    raise Exception(f"StreamableFunction {self._stream.__name__} returned UNSET")
                else:
                    logger.warning(f"StreamableFunction {self._stream.__name__} returned UNSET")
                    self.set_cache(key, (cached_stream, None))
            else:
                self.set_cache(key, (cached_stream, item))
        finally:
            if DEV and stream_completed:
                # Checks if the iterator hit break, or if it actually errored
                current_frame = inspect.currentframe()
                if previous_frame := current_frame.f_back:
                    frame_info = inspect.getframeinfo(previous_frame)
                    line = frame_info.code_context[0].strip()
                    if line == "break":
                        logger.debug(f"StreamableFunction {self._stream.__name__} hit break, no error")
                        return item
                self.delete_cache(key)
        return item

    def __call__(self, *args: InputType.args, **kwargs: InputType.kwargs) -> YieldType | ReturnType:
        """
        Returns the last yield or return result of the stream
        """
        return last(self.stream(*args, **kwargs))


Streamable: TypeAlias = Generator[YieldType, None, YieldType]
StreamableWithReturn: TypeAlias = Generator[YieldType, None, ReturnType]


def streamable(
    stream: Callable[InputType, Generator[YieldType, None, ReturnType]]
) -> StreamableFunction[InputType, ReturnType, YieldType]:
    return StreamableFunction(stream)


def cached_streamable(cache: Cache, ignore_params: list[str] = []) -> Callable[
    [Callable[InputType, Generator[YieldType, None, ReturnType]]],
    StreamableFunction[InputType, ReturnType, YieldType],
]:
    def decorator(
        stream: Callable[InputType, Generator[YieldType, None, ReturnType]]
    ) -> StreamableFunction[InputType, ReturnType, YieldType]:
        return StreamableFunction(stream, cache, ignore_params)

    return decorator


if __name__ == "__main__":

    @streamable
    def stream() -> Streamable[int]:
        for i in range(10):
            yield i
        return -1

    result = stream()
    print(result)

    for message in stream.stream():
        print(message)
