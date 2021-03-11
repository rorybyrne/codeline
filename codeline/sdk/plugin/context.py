"""Code Context

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Line:
    number: int
    text: str

    def __contains__(self, item: str):
        return item in self.text

    def __str__(self):
        truncate_at = 75
        text = (self.text[:truncate_at] + '..') if len(self.text) > truncate_at else self.text
        return f"[{self.number}: '{text.rstrip()}']"


@dataclass
class Context:
    lines: List[Line]
    command_index: int

    def clean(self, line: Line):
        """Removes the Codeline command from the line"""
        line_parts = line.text.strip().split('#')
        if len(line_parts) == 3:
            line.text = line_parts[0]
        else:
            raise RuntimeError("Line must have an inline comment (and no other # symbols)")

        self._write(line)

    def _write(self, line: Line):
        raise NotImplementedError("This is not implemented in the SDK")
