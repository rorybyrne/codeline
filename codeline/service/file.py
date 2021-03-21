"""File service

Author: Rory Byrne <rory@rory.bio>
"""

from pathlib import Path
from typing import List

from codeline.sdk.context.file import File
from codeline.sdk.context.line import CommandLine, Line
from codeline.sdk.util import regex


class FileService:
    """Functionality for processing files"""

    def read(self, file_path: Path) -> File:
        """Read the file into Line instances"""
        if not file_path.is_file():
            raise RuntimeError(f"{str(file_path)} is not a file.")

        with open(file_path) as f:
            lines = f.readlines()

            return self._from_lines(file_path, lines)

    # Private #####################################################################################

    def _build_line(self, raw: str) -> Line:
        """Construct either a regular Line or a CommandLine, depending on the content of the line"""
        line = self._clean_line(raw)
        try:
            command, tail = regex.extract_command_and_tail(line)
            if tail and '|' in tail:  # Implies the command has a response, which is unexpected
                raise ValueError(f"The tail contains an invalid character, '|': {line}")
            return CommandLine(line, command, tail)
        except ValueError:
            return Line(line)

    def _from_lines(self, file: Path, lines: List[str]) -> File:
        """Construct a File from a list of raw lines"""
        parsed_lines = [self._build_line(line) for i, line in enumerate(lines)]
        return File(parsed_lines, file)

    @staticmethod
    def _clean_line(line: str) -> str:
        """Pre-process a line"""
        return line.rstrip()
