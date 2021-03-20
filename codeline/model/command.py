"""Command model

Author: Rory Byrne <rory@rory.bio>
"""
import logging
from dataclasses import dataclass

from codeline.model.pluginmeta import PluginMeta
from codeline.sdk.context.context import Context

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
