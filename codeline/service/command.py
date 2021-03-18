"""Command service

Author: Rory Byrne <rory@rory.bio>
"""
import logging
from argparse import ArgumentParser
import shlex
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

    def process_file(self, file_path: str):
        """Process a file into commands, and run those commands"""
        file = self._file.read(file_path)
        commands = self._parse_commands(file)

        for command in commands:
            self._run_command(command)

    # Private ###############################################################################

    def _run_command(self, command: Command):
        writer = Writer(command.context.file.path)
        command.context.set_writer(writer)
        kwargs = self._parse_args(command)

        try:
            result = command.plugin.invoke(command.context, **kwargs)
            if not result.successful:
                log.debug("Command failed.")
            else:
                log.debug("Command successful.")
            log.debug(result.message)
        except PluginException as e:
            log.exception(e)
            command.context.write_response(str(e))
            raise
        except Exception:
            command.context.write_response("An unknown error occurred")
            raise

    def _parse_args(self, command: Command):
        parser = ArgumentParser(command.plugin.title)
        command.plugin.implementation.define_arguments(parser)

        print(f"Parsing: '{shlex.split(command.options)}'")
        namespace = parser.parse_args(shlex.split(command.options))
        return vars(namespace)

    def _parse_commands(self, file: File) -> List[Command]:
        """Parse the file into a list of Commands"""
        return [
            command
            for i, _ in enumerate(file)
            if (command := catch(lambda: self._parse_command(file, i))) is not None  # Note the catch
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
        else:
            raise ValueError(f"Line is not a command-line: {line}")

    @staticmethod
    def _build_context(file: File, line_no: int) -> Context:
        """Build a context for the plugin to receive"""
        return Context(file, line_no)
