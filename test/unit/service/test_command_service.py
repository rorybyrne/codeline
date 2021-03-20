from pathlib import Path
from unittest.mock import patch

import pytest

from codeline.service.command import CommandService
from codeline.service.file import FileService

SOURCE_COMMAND = """def my_function(input: str):
    # <| test "hello"
    do_something(input)
    with open(str) as f: # ~$ echo "inline trigger"
        f.write(input)
"""

SOURCE_NO_COMMAND = """def my_function(input: str):
    do_something(input)
    with open(str) as f:
        f.write(input)
"""


class TestCommandService:
    @pytest.fixture
    @patch('codeline.service.plugin.PluginService')
    @patch('codeline.service.file.FileService')
    def command_service(self, mock_fs, mock_ps) -> CommandService:
        return CommandService(mock_ps, mock_fs)

    @pytest.fixture
    def file_service(self):
        return FileService()

    def test_parse_file_success(self, command_service: CommandService, file_service: FileService):
        raw_lines = SOURCE_COMMAND.split('\n')
        file = file_service._from_lines(Path('.'), raw_lines)

        commands = command_service._parse_commands(file)

        assert commands is not None and len(commands) == 1

    def test_parse_file_failure_no_command(self, command_service, file_service: FileService):
        raw = SOURCE_NO_COMMAND.split('\n')
        file = file_service._from_lines(Path('.'), raw)

        commands = command_service._parse_commands(file)

        assert len(commands) == 0
