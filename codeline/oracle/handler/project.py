"""Project event handler

Author: Rory Byrne <rory@rory.bio>
"""

from watchdog.events import FileSystemEvent

from codeline.oracle.handler.base import BaseEventHandler
from codeline.service.command import CommandService
from codeline.util.log import Logger


class ProjectEventHandler(BaseEventHandler, Logger):

    def __init__(self, command_service: CommandService, file_service):
        super().__init__()
        assert command_service
        assert file_service
        self._command = command_service
        self._file = file_service

    def on_modified(self, event: FileSystemEvent):
        """Handle modification events

        0. Ignore if it's in .gitignore
        1. Check if it's a file modification
        2. Parse the file into a list of Command instances

        @param event: The event
        """
        event_path = event.src_path
        if not self._file.is_file(event_path):
            return
        elif not event_path.endswith('.py'):
            return
        else:
            print(f'Got file {event_path}')
            self._command.process_file(event_path)
