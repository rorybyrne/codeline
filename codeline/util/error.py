"""Error utils

Author: Rory Byrne <rory@rory.bio>
"""
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def catch(fn: Callable, to_return=None):
    """Utility for catching exceptions in a list comprehension"""
    try:
        return fn()
    except Exception:
        return to_return
