"""Regex Utils

Author: Rory Byrne <rory@rory.bio>
"""
import re
from typing import Tuple, Optional


class Comment:
    PYTHON = r"^\s*# [^\n\r]+"


class CommandRegex:
    PYTHON = r"^\s*\# <\| ([a-z]+) ([^\r\n]+)?"  # (command) (everything else)

    @staticmethod
    def extract_command_and_tail(line: str) -> Tuple[str, Optional[str]]:
        """Returns the command and tail from a line, or raises an Exception"""
        regexp = re.compile(CommandRegex.PYTHON)
        search = regexp.search(line)
        if not search:
            raise ValueError(f"Not a command: {line}")

        command: Optional[str] = search.group(1)
        tail: Optional[str] = search.group(2)
        if not command:
            raise ValueError(f"No command found: {line}")

        return command, tail
