"""Base Event Handler

Author: Rory Byrne <rory@rory.bio>
"""

from cachetools import LRUCache
from watchdog.events import FileSystemEventHandler  # type: ignore


class BaseEventHandler(FileSystemEventHandler):
    """Event handler with a cache"""
    def __init__(self):
        self._cache = LRUCache(256)
