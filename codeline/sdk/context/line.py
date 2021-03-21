"""Line

Author: Rory Byrne <rory@rory.bio>
"""
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Line(ABC):
    """Model of a line of source code

    Attrs:
        number      The line's number in the file
        text        The literal content of the line
    """
    _text: str

    def __contains__(self, item: str):
        return item in self._text

    def __str__(self):
        return self._text

    @property
    def text(self):
        """The text of the line"""
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value


@dataclass
class CommandLine(Line):
    """Model of a line of source code containing a command

    Attrs:
        command         The trigger word for the command
        options         The options passed to the command
        response        The response that the plugin has currently set for the coder
    """
    _command: str
    _options: Optional[str]
    _response: Optional[str] = field(init=False, default=None)

    def __str__(self) -> str:
        return f'{self._text} | {self._response}'

    @property
    def response(self) -> Optional[str]:
        """The response message in the command line"""
        return self._response

    @response.setter
    def response(self, response: str):
        self._response = response

    @property
    def command(self) -> str:
        """The command word"""
        return self._command

    @property
    def options(self) -> Optional[str]:
        """The options passed to the command"""
        return self._options
