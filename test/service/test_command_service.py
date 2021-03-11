from unittest.mock import patch

import pytest

from codeline.model.file import File, Line
from codeline.service.command import CommandService
from codeline.service.file import FileService
from codeline.service.plugin import PluginService

SOURCE_CODE = """def my_function(input: str):
    # ~$ echo "hello"
    do_something(input)
    with open(str) as f: # ~$ echo "inline trigger"
        f.write(input)
"""


class TestCommandService:
    @pytest.fixture
    @patch('codeline.service.plugin.PluginService')
    @patch('codeline.service.file.FileService')
    def command_service(self, mock_fs, mock_ps):
        return CommandService(mock_ps, mock_fs)

    def test_parse_file_success(self, command_service):
        raw_lines = SOURCE_CODE.split('\n')
        file = File.from_lines('/tmp/somewhere', raw_lines)

        commands = command_service._parse_commands(file)

        assert commands is not None

    def test_extract_command_success(self, command_service):
        line = Line(0, "    # ~$ echo 'howdy'")
        raw_command = command_service._extract_raw_command(line)
        assert isinstance(raw_command, str)

    # def test_process_file_success(self):
    #     fs = FileService()
    #     ps = PluginService('/home/rory/projects/personal/codeline/dev/plugins')
    #     cs = CommandService(ps, fs)
    #     print(cs)
    #
    #     file = '/home/rory/projects/personal/codeline/dev/source.py'
    #     cs.process_file(file)


