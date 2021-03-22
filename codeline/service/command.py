"""Command service

Author: Rory Byrne <rory@rory.bio>
"""

import logging
import shlex
from argparse import ArgumentParser
from pathlib import Path
from typing import List

from codeline.model.command import Command
from codeline.model.writer import Writer
from codeline.sdk.context.context import Context
from codeline.sdk.context.file import File
from codeline.sdk.context.line import CommandLine
from codeline.sdk.exception import PluginException
from codeline.service.file import FileService
from codeline.service.plugin import PluginService
from codeline.util.error import catch

log = logging.getLogger(__name__)


class CommandService:
    """Functionality for running Codeline commands"""

    def __init__(self, plugin_service: PluginService, file_service: FileService):
        super().__init__()
        assert plugin_service
        assert file_service
        self._plugin = plugin_service
        self._file = file_service

    def process_file(self, file_path: Path):
        """Process a file into commands, and run those commands"""
        file = self._file.read(file_path)
        commands = self._parse_commands(file)

        for command in commands:
            self.run_command(command)

    def run_command(self, command: Command):
        """Runs the given command"""
        writer = Writer(command.context.file.path)
        command.context.set_writer(writer)

        try:
            kwargs = self._parse_args(command)
            result = command.plugin.invoke(command.context, **kwargs)
            if not result.successful:
                log.debug("Command failed.")
            else:
                log.debug("Command successful.")
            log.debug(result.message)
        except PluginException as e:
            log.debug(e, exc_info=True, stack_info=True)
            command.context.write_response(str(e))
        except Exception:
            command.context.write_response("An unknown error occurred")
            raise
        except SystemExit:  # We should subclass ArgumentParser for better error handling
            command.context.write_response("Invalid arguments")

    # Private ###############################################################################

    @staticmethod
    def _parse_args(command: Command):
        if not command.options:
            return {}

        parser = ArgumentParser(command.plugin.title)
        command.plugin.implementation.define_arguments(parser)

        namespace = parser.parse_args(shlex.split(command.options))
        return vars(namespace)

    def _parse_commands(self, file: File) -> List[Command]:
        """Parse the file into a list of Commands"""
        return [
            command
            for i, _ in enumerate(file)
            # pylint: disable=cell-var-from-loop
            if (command := catch(lambda: self._parse_command(file, i), to_catch=ValueError)) is not None
        ]

    def _parse_command(self, file: File, line_no: int) -> Command:
        """Build a Command from a line of source code"""
        line = file[line_no]
        if isinstance(line, CommandLine):
            trigger = line.command
            options = line.options
            context = self._build_context(file, line_no)
            plugin = self._plugin.get_plugin_for_trigger(trigger)

            return Command(trigger, options, plugin, context)

        raise ValueError(f"Line is not a command-line: {line}")

    @staticmethod
    def _build_context(file: File, line_no: int) -> Context:
        """Build a contextefor the plugin to receive"""
        return Context(file, line_no)
