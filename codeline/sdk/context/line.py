"""Line

Author: Rory Byrne <rory@rory.bio>
"""
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Line(ABC):
    number: int
    _text: str

    def __contains__(self, item: str):
        return item in self._text

    def __str__(self):
        return self._text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value


@dataclass
class CommandLine(Line):
    _command: str
    _options: str
    _response: Optional[str] = field(init=False, default=None)

    def __str__(self):
        return f'{self._text} | {self._response}'

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: str):
        self._response = response

    @property
    def command(self):
        return self._command

    @property
    def options(self):
        return self._options
