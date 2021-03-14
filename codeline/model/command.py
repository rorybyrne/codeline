"""Command model

Author: Rory Byrne <rory@rory.bio>
"""
from codeline.util.log import Logger
from dataclasses import dataclass

from codeline.model.pluginmeta import PluginMeta
from codeline.model.writer import Writer
from codeline.sdk.context.context import Context
from codeline.sdk.exception import PluginException


@dataclass
class Command(Logger):
    """Models a command to be run by Codeline

    Attrs:
        trigger     The command's trigger word
        options     Options passed to the command
        plugin      Metadata for the plugin, including a reference to its implementation
        context     Context about the command to be passed into the plugin when it runs
    """
    trigger: str
    options: str
    plugin: PluginMeta
    context: Context

    def __post_init__(self):
        super().__init__()

    def __str__(self):
        return f'Command[ {self.trigger} ]'

    def run(self, file_path: str):
        """Run the command

        Attaches a writer to the context and then invokes the plugin
        """
        writer = Writer(file_path)
        self.context.set_writer(writer)
        try:
            result = self.plugin.invoke(self.context)
            if not result.successful:
                self.log.debug("Command failed.")
            else:
                self.log.debug("Command successful.")
            self.log.debug(result.message)
        except PluginException as e:
            self.log.exception(e)
            raise
