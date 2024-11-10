# pylint: disable=all
import sys
from bdb import BdbQuit
from contextlib import contextmanager


@contextmanager
def post_mortem():
    try:
        yield
    except BdbQuit:
        raise
    except Exception as e:
        import pdb  # noqa: T100

        pdb.post_mortem()
        raise e


@contextmanager
def bp():
    try:
        yield
    except BdbQuit:
        raise
    except Exception as e:
        # goes 3 frames back
        import pdb  # noqa: T100

        frame = sys._getframe()
        for _ in range(2):
            if frame.f_back:
                frame = frame.f_back
        pdb.Pdb().set_trace(frame)
        raise e
