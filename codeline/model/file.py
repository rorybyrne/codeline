"""File model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from typing import List, Union

from codeline.sdk.plugin.context import Line, Context


@dataclass
class File:
    path: str
    lines: List[Line]

    def __getitem__(self, item: int) -> Union[Line, List[Line]]:
        return self.lines.__getitem__(item)

    def __setitem__(self, index: int, value: Line):
        if not isinstance(index, int):
            raise TypeError("Must index a file with an integer value")
        elif not isinstance(value, Line):
            raise TypeError("Expected a Line instance")

        self.lines[index] = value

    def __iter__(self):
        return self.lines.__iter__()

    def __len__(self):
        return len(self.lines)

    def __str__(self):
        return f'[File: {len(self.lines)} lines]'

    def get_context(self, line: Line, down: int = 5, up: int = 5) -> Context:
        """Returns a context of nearby lines for the given line of the file"""
        command_index = line.number
        start_index = (command_index - up) if command_index > up else 0
        end_index = (command_index + down) if command_index + down < len(self) else len(self)

        lines = self[start_index:end_index]

        return Context(lines, command_index)

    @staticmethod
    def from_lines(path: str, lines: List[str]):
        lines = [Line(i, line) for i, line in enumerate(lines)]
        return File(path, lines)
