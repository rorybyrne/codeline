"""Code Context

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field
from typing import List, Any, Optional

from codeline.sdk.context.file import File
from codeline.sdk.context.line import Line, CommandLine

Writer = Any  # Implemented in Codeline


@dataclass
class Context:
    """The context in which your plugin runs

    Provides useful methods for interacting with the code, and responding to the coder.

    Attrs:
        file                The file in which the command was run
        _command_index      The line number where the command is
        _writer             An object used by Codeline to update the file
    """
    file: File
    _command_index: int
    _writer: Writer = field(init=False, default=None)

    @property
    def command_line(self) -> CommandLine:
        """Returns the line which contains the command"""
        line = self.file[self._command_index]
        if not isinstance(line, CommandLine):
            raise RuntimeError("The command_line is not an instance of CommandLine")

        return line

    @property
    def command_index(self):
        """Returns the line number where the command appears"""
        return self._command_index

    def write_response(self, message: str):
        """Writes a response message to the coder"""
        cmd_line = self.command_line

        cmd_line.response = message
        self.write()

    def write_lines(self, lines: List[str]):
        """Write new lines into the source code, underneath the command line"""
        index = self._command_index + 1
        for raw in lines:
            line = Line(raw.rstrip())
            self.file.lines.insert(index, line)
            index += 1

        self.write()

    def clear(self):
        """Clear your command from the source code"""
        del self.file[self._command_index]

        self.write()

    def set_writer(self, writer: Writer):
        """Sets the writer. Not intended for Plugins"""
        self._writer = writer

    def write(self, file: Optional[File] = None):
        if not self._writer:
            raise ValueError("Writer is none")

        if not file:
            file = self.file

        self._writer.write(file)
