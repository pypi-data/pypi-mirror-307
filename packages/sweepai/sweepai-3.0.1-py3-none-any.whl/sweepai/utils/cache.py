import hashlib
import inspect
import os
import pickle
import time

from diskcache import Cache
from loguru import logger

from sweepai.config.server import CACHE_DIRECTORY, FILE_CACHE_DISABLED

TEST_BOT_NAME = "sweep-nightly[bot]"
MAX_DEPTH = 10
# if DEBUG:
#     logger.debug("File cache is disabled.")


def recursive_hash(value, depth=0, ignore_params=[]):
    """Hash primitives recursively with maximum depth."""
    if depth > MAX_DEPTH:
        return hashlib.md5("max_depth_reached".encode()).hexdigest()

    if isinstance(value, (int, float, str, bool, bytes)):
        return hashlib.md5(str(value).encode()).hexdigest()
    elif isinstance(value, (list, tuple)):
        return hashlib.md5(
            "".join([recursive_hash(item, depth + 1, ignore_params) for item in value]).encode()
        ).hexdigest()
    elif isinstance(value, dict):
        return hashlib.md5(
            "".join(
                [
                    recursive_hash(key, depth + 1, ignore_params) + recursive_hash(val, depth + 1, ignore_params)
                    for key, val in value.items()
                    if key not in ignore_params
                ]
            ).encode()
        ).hexdigest()
    elif hasattr(value, "cache_key") and value.cache_key:
        return value.cache_key
    elif hasattr(value, "__dict__") and value.__class__.__name__ not in ignore_params:
        return recursive_hash(value.__dict__, depth + 1, ignore_params)
    else:
        return hashlib.md5("unknown".encode()).hexdigest()


def hash_code(code):
    return hashlib.md5(code.encode()).hexdigest()


def file_cache(ignore_params=[], ignore_contents=False, verbose=False):
    """Decorator to cache function output based on its inputs, ignoring specified parameters.
    Ignore parameters are used to avoid caching on non-deterministic inputs, such as timestamps.
    We can also ignore parameters that are slow to serialize/constant across runs, such as large objects.
    """

    def decorator(func):
        if FILE_CACHE_DISABLED:
            return func
        func_source_code_hash = hash_code(inspect.getsource(func)) if not ignore_contents else ""

        def wrapper(*args, **kwargs):
            if kwargs.get("do_not_use_file_cache", False):
                return func(*args, **kwargs)
            cache_dir = CACHE_DIRECTORY + "/file_cache"
            os.makedirs(cache_dir, exist_ok=True)
            result = None

            # Convert args to a dictionary based on the function's signature
            args_names = func.__code__.co_varnames[: func.__code__.co_argcount]
            args_dict = dict(zip(args_names, args))

            # Remove ignored params
            kwargs_clone = kwargs.copy()
            for param in ignore_params:
                args_dict.pop(param, None)
                kwargs_clone.pop(param, None)

            # Create hash based on function name, input arguments, and function source code
            arg_hash = (
                recursive_hash(args_dict, ignore_params=ignore_params)
                + recursive_hash(kwargs_clone, ignore_params=ignore_params)
                + func_source_code_hash
            )
            cache_key = f"{func.__module__}_{func.__name__}_{arg_hash}"
            cache_file = os.path.join(cache_dir, f"{cache_key}.pickle")
            try:
                # If cache exists, load and return it
                if os.path.exists(cache_file):
                    if verbose:
                        print("Used cache for function: " + func.__name__)
                    with open(cache_file, "rb") as f:
                        result = pickle.load(f)
            except Exception:
                logger.info("Unpickling failed")
            # Otherwise, call the function and save its result to the cache
            if result is None:
                result = func(*args, **kwargs)
            # hydrate both caches in all cases
            if isinstance(result, Exception):
                logger.info(f"Function {func.__name__} returned an exception")
            elif not os.path.exists(cache_file):
                try:
                    with open(cache_file, "wb") as f:
                        pickle.dump(result, f)
                except Exception as e:
                    logger.info(f"Pickling failed: {e}")
            return result

        return wrapper

    return decorator


def create_cache_from_file(file_path: str):
    return Cache(f"{CACHE_DIRECTORY}/{os.path.splitext(os.path.basename(file_path))[0]}")


def create_cache():
    file = os.path.relpath(inspect.currentframe().f_back.f_code.co_filename)
    return create_cache_from_file(file)


if __name__ == "__main__":

    @file_cache()
    def test_func(a, b):
        time.sleep(3)
        return a + b

    print("Running...")
    print(test_func(1, 1))
    print("Running again")
    print(test_func(1, 1))
    print("Done")
