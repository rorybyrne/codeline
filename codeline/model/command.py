"""Command model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass

from codeline.model.file import Context
from codeline.model.plugin import Plugin


@dataclass
class Command:
    raw: str
    plugin: Plugin
    context: Context

    def run(self):
        result = self.plugin.invoke(self.context)
        if not result.successful:
            print("Command failed.")
        else:
            print("Command successful.")
        print(result.message)
