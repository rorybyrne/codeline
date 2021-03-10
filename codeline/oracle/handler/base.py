"""Base Event Handler

Author: Rory Byrne <rory@rory.bio>
"""
from cachetools import LRUCache
from watchdog.events import FileSystemEventHandler


class BaseEventHandler(FileSystemEventHandler):
    def __init__(self):
        self._cache = LRUCache(256)
