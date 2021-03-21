"""Project event handler

Author: Rory Byrne <rory@rory.bio>
"""

import logging
from pathlib import Path

from watchdog.events import FileSystemEvent  # type: ignore

from codeline.oracle.handler.base import BaseEventHandler
from codeline.service.command import CommandService
from codeline.service.file import FileService

log = logging.getLogger(__name__)


class ProjectEventHandler(BaseEventHandler):
    """Handle changes in a project directory"""

    def __init__(self, command_service: CommandService, file_service: FileService):
        super().__init__()
        assert command_service
        assert file_service
        self._command = command_service
        self._file = file_service

    def on_modified(self, event: FileSystemEvent):
        """Handle modification events"""
        event_path = Path(event.src_path)
        if not event_path.is_file():
            return

        if event_path.suffix != '.py':
            return

        log.debug(f'READING -> {event_path}')
        self._command.process_file(event_path)
