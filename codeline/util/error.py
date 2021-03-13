"""Error utils

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Callable


def catch(fn: Callable, to_return=None):
    try:
        return fn()
    except Exception:
        return to_return
