"""Code Context

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field
from typing import List, Any

from codeline.sdk.context.file import File
from codeline.sdk.context.line import Line, CommandLine

Writer = Any  # Implemented in Codeline


@dataclass
class Context:
    file: File
    _command_index: int
    _writer: Writer = field(init=False, default=None)

    @property
    def command_line(self) -> CommandLine:
        line = self.file[self._command_index]
        if not isinstance(line, CommandLine):
            raise RuntimeError("The command_line is not an instance of CommandLine")

        return line

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self, writer: Writer):
        if not writer:
            raise ValueError("Writer is none")

        self._writer = writer

    def write(self):
        if not self._writer:
            raise ValueError("Writer is none")

        self._writer.write(self.file)

    def write_response(self, message: str):
        """Writes a response message into the comment"""
        cmd_line = self.command_line

        cmd_line.response = message
        self.write()

    def write_lines(self, lines: List[str]):
        index = self._command_index + 1
        for raw in lines:
            line = Line(index, raw.rstrip())
            self.file.lines.insert(index, line)
            index += 1

        self.write()

    def clear(self):
        del self.file[self._command_index]

        self.write()
