"""Command model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass

from codeline.model.pluginmeta import PluginMeta
from codeline.model.writer import Writer
from codeline.sdk.context.context import Context
from codeline.sdk.exception import PluginException


@dataclass
class Command:
    trigger: str
    options: str
    plugin: PluginMeta
    context: Context

    def __str__(self):
        return f'Command[ {self.trigger} ]'

    def run(self, file_path: str):
        print('\n')
        writer = Writer(file_path)
        self.context.writer = writer
        try:
            result = self.plugin.invoke(self.context)
            if not result.successful:
                print("Command failed.")
            else:
                print("Command successful.")
            print(result.message)
        except PluginException as e:
            print(e)
            raise
