"""Command service

Author: Rory Byrne <rory@rory.bio>
"""
from typing import List

from codeline.model.command import Command
from codeline.model.file import File, Line
from codeline.service.file import FileService
from codeline.service.plugin import PluginService
from codeline.util.log import Logger


class CommandService(Logger):
    """Parsing and executing commands"""

    TRIGGER = '~$'
    COMMENT_PYTHON = '#'

    def __init__(self, plugin_service: PluginService, file_service: FileService):
        super().__init__()
        assert plugin_service
        assert file_service
        self._plugin = plugin_service
        self._file = file_service

    def process_file(self, file_path: str):
        self.log.debug(f"Processing {file_path}")
        file = self._file.read(file_path)
        commands = self._parse_commands(file)
        self.log.debug(f'Got {len(commands)} commands in file {file_path}.')
        for command in commands:
            command.run()

    # Private ###############################################################################

    def _parse_commands(self, file: File) -> List[Command]:
        """Parse the file into a list of Commands"""
        return [self._parse_command(file, line) for line in file if self._has_command(line)]

    def _parse_command(self, file: File, line: Line) -> Command:
        """Build a Command from a line of source code"""
        context = file.get_context(line)
        raw_command = self._extract_raw_command(line)
        trigger = raw_command.split(' ')[0]
        plugin = self._plugin.get_plugin_for_trigger(trigger)

        return Command(raw_command, plugin, context)

    def _extract_raw_command(self, line: Line):
        """Extract the content of the command from the line"""
        if CommandService.TRIGGER not in line:
            raise ValueError(f"Invalid line: {line}")

        return line.text\
            .replace(CommandService.COMMENT_PYTHON, '') \
            .replace(CommandService.TRIGGER, '') \
            .strip()

    def _has_command(self, line: Line) -> bool:
        """Check whether this line of code contains a command"""
        has_trigger = CommandService.TRIGGER in line
        raw_line = line.text.replace(CommandService.COMMENT_PYTHON, '').strip()
        trigger_is_inline = not raw_line.startswith(CommandService.TRIGGER)
        if has_trigger and trigger_is_inline:
            self.log.debug(f'Ignoring inline trigger: {line}')
            return False

        return has_trigger
