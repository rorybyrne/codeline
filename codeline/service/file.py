"""File service

Author: Rory Byrne <rory@rory.bio>
"""
import os
from typing import List

from codeline.sdk.context.file import File
from codeline.sdk.context.line import CommandLine, Line
from codeline.sdk.util.regex import CommandRegex
from codeline.util.log import Logger


class FileService(Logger):
    """Functionality for processing files"""

    def read(self, file_path: str) -> File:
        """Read the file into Line instances"""
        if not FileService.is_file(file_path):
            raise RuntimeError(f"{file_path} is not a file.")

        with open(file_path) as f:
            lines = f.readlines()

            return self._from_lines(lines)

    @staticmethod
    def is_file(path: str) -> bool:
        """Check if the path is a file"""
        return os.path.isfile(path)

    # Private #####################################################################################

    def _build_line(self, index: int, raw: str):
        """Construct either a regular Line or a CommandLine, depending on the content of the line"""
        line = self._clean_line(raw)
        try:
            command, tail = CommandRegex.extract_command_and_tail(line)
            if '|' in tail:  # Implies the command has a response, which is unexpected
                raise ValueError(f"The tail contains an invalid character, '|': {line}")
            return CommandLine(index, line, command, tail)
        except Exception:
            return Line(index, line)

    def _from_lines(self, lines: List[str]) -> File:
        """Construct a File from a list of raw lines"""
        lines = [self._build_line(i + 1, line) for i, line in enumerate(lines)]
        return File(lines)

    @staticmethod
    def _clean_line(line: str) -> str:
        """Pre-process a line"""
        return line.rstrip()
