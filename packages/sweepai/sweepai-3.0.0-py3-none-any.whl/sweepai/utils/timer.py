import time
from dataclasses import dataclass

from loguru import logger


@dataclass
class Timer:
    name: str = ""
    min_time: float = 0.01
    start: float = 0
    end: float = 0
    time_elapsed: float = -1
    do_print: bool = True
    precision: int = 2

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        self.time_elapsed = self.end - self.start
        if self.do_print and self.time_elapsed > self.min_time:
            if self.name:
                logger.debug(f"Timer {self.name} elapsed: {self.time_elapsed:.{self.precision}f} seconds")
            else:
                logger.debug(f"Timer elapsed: {self.time_elapsed:.{self.precision}f} seconds")


if __name__ == "__main__":
    with Timer() as t:
        time.sleep(1)
    print(t.time_elapsed)
    assert t.time_elapsed > 0.9
