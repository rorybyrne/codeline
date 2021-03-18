"""Project event handler

Author: Rory Byrne <rory@rory.bio>
"""

from watchdog.events import FileSystemEvent

from codeline.oracle.handler.base import BaseEventHandler
from codeline.service.command import CommandService
from codeline.service.file import FileService


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
        event_path = event.src_path
        if not self._file.is_file(event_path):
            return
        elif not event_path.endswith('.py'):
            return
        else:
            self._command.process_file(event_path)
