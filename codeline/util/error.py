"""Error utils

Author: Rory Byrne <rory@rory.bio>
"""

import logging
from typing import Callable

logger = logging.getLogger(__name__)


def catch(func: Callable, to_return=None, to_catch=RuntimeError):
    """Utility for catching exceptions in a list comprehension"""
    try:
        return func()
    except to_catch:
        return to_return
