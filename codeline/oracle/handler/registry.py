"""Registry event handler

Author: Rory Byrne <rory@rory.bio>
"""

from typing import Tuple, Callable

from time import time
from watchdog.events import FileSystemEvent

from codeline.oracle.handler.base import BaseEventHandler
from codeline.service.registry import RegistryService
from codeline.util.log import Logger

TimedEvent = Tuple[int, str]


class RegistryEventHandler(BaseEventHandler, Logger):
    """Handle changes to the projects registry"""

    def __init__(self, registry_service: RegistryService):
        super().__init__()
        self._registry_service = registry_service
        self._handler = None

    def on_created(self, event: FileSystemEvent):
        """Pass the event to the Guru to update the plan state"""
        assert self._handler, "Registry event handler missing"
        if self._should_handle(event):
            projects = self._registry_service.load_projects()
            project_dirs = [p.root_dir for p in projects]
            self._handler(project_dirs)

    def on_modified(self, event: FileSystemEvent):
        """Handles the modification event"""
        assert self._handler, "Registry event handler missing"
        if self._should_handle(event):
            projects = self._registry_service.load_projects()
            project_dirs = [p.root_dir for p in projects]
            self._handler(project_dirs)

    def set_handler(self, handler: Callable):
        if not handler:
            raise ValueError("Cannot assign a None handler")
        self._handler = handler

    def _should_handle(self, event: FileSystemEvent):
        """Determine whether or not we should handle this event, or skip it

        Notes:
            There might be a race condition when the `seconds` value is at x.99999
        """
        seconds = int(time())
        if not event.is_directory and event.src_path.endswith("projects.json"):
            return False

        timed_event = (seconds, event.src_path)
        is_duplicate = timed_event in self._cache
        if is_duplicate:
            self._cache[timed_event] = event
            return False

        return True
