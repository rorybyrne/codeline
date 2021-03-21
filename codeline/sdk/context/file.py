"""File

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from codeline.sdk.context.line import Line


@dataclass
class File:
    """Model of a file, containing lines of source code"""
    lines: List[Line]
    path: Path

    def __getitem__(self, item: int) -> Union[Line, List[Line]]:
        return self.lines.__getitem__(item)

    def __setitem__(self, index: int, value: Line):
        if not isinstance(index, int):
            raise TypeError("Must index a file with an integer value")

        if not isinstance(value, Line):
            raise TypeError("Expected a Line instance")

        self.lines[index] = value

    def __delitem__(self, item: int):
        del self.lines[item]

    def __iter__(self):
        return self.lines.__iter__()

    def __len__(self):
        return len(self.lines)

    def __str__(self):
        return '\n'.join([str(line) for line in self.lines])
