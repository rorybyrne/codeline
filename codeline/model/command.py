"""Command model

Author: Rory Byrne <rory@rory.bio>
"""
import logging
from dataclasses import dataclass

from codeline.model.pluginmeta import PluginMeta
from codeline.model.writer import Writer
from codeline.sdk.context.context import Context
from codeline.sdk.exception import PluginException

log = logging.getLogger(__name__)


@dataclass
class Command:
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
                log.debug("Command failed.")
            else:
                log.debug("Command successful.")
            log.debug(result.message)
        except PluginException as e:
            log.exception(e)
            self.context.write_response(str(e))
            raise
