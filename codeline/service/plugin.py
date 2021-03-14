"""Plugin service

Author: Rory Byrne <rory@rory.bio>
"""
import importlib
import importlib.util
import os
from typing import Type

import sys

from codeline.exceptions import PluginImplementationException, PluginNotFoundException
from codeline.model.pluginmeta import PluginMeta
from codeline.sdk import CodelinePlugin
from codeline.util.log import Logger


class PluginService(Logger):
    """Loading plugins"""

    def __init__(self, plugin_directory: str):
        super().__init__()
        sys.path.insert(0, plugin_directory)
        loaded_plugins = self._load_all_plugins(plugin_directory)
        self._plugins = {plugin.trigger: plugin for plugin in loaded_plugins}

    def get_plugin_for_trigger(self, trigger: str) -> PluginMeta:
        plugin = self._plugins.get(trigger)
        if not plugin:
            raise PluginNotFoundException(trigger)

        return plugin

    @staticmethod
    def _load_plugin(plugin_name: str) -> PluginMeta:
        entrypoint = '.'.join([plugin_name, 'main'])
        module = importlib.import_module(entrypoint)
        klass: Type[CodelinePlugin] = getattr(module, 'Plugin', None)
        if not klass:
            raise PluginImplementationException(f"Could not load plugin: {plugin_name}")

        return PluginMeta(plugin_name, klass())

    def _load_all_plugins(self, directory: str):
        plugin_dirs = [plugin for plugin in os.listdir(directory) if not plugin.endswith('.py')]
        loaded_plugins = [self._load_plugin(plugin) for plugin in plugin_dirs]
        return loaded_plugins
