"""Plugin service

Author: Rory Byrne <rory@rory.bio>
"""
from codeline.util.error import catch
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
    """Functionality to load and handle plugins"""

    def __init__(self, plugin_directory: str):
        """Load plugins on-startup"""
        super().__init__()
        sys.path.insert(0, plugin_directory)
        loaded_plugins = self._load_all_plugins(plugin_directory)
        self._plugins = {plugin.trigger: plugin for plugin in loaded_plugins}

    def get_plugin_for_trigger(self, trigger: str) -> PluginMeta:
        """Find the right plugin for a given command trigger"""
        plugin = self._plugins.get(trigger)
        if not plugin:
            raise PluginNotFoundException(trigger)

        return plugin

    @staticmethod
    def _load_plugin(plugin_name: str) -> PluginMeta:
        """Load a plugin which is already on the path

        Args:
            plugin_name     The name of the plugin's main directory

        Returns:
            PluginMeta      An object describing the plugin, including a reference to its instance

        Raises:
            PluginImplementationException   The plugin cannot be loaded
        """
        entrypoint = '.'.join([plugin_name, 'main'])
        module = importlib.import_module(entrypoint)
        klass: Type[CodelinePlugin] = getattr(module, 'Plugin', None)
        if not klass:
            raise PluginImplementationException(f"Could not load plugin: {plugin_name}")

        return PluginMeta(plugin_name, klass())

    def _load_all_plugins(self, directory: str):
        """Finds all likely-plugins in the plugin directory and loads them"""
        plugin_dirs = [plugin for plugin in os.listdir(directory) if not plugin.endswith('.py')]
        loaded_plugins = [
            loaded_plugin for plugin in plugin_dirs
            if (loaded_plugin := catch(lambda: self._load_plugin(plugin))) is not None  # Note the catch
        ]

        return loaded_plugins
