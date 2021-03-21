"""Plugin service

Author: Rory Byrne <rory@rory.bio>
"""

import importlib
import importlib.util
import logging
import sys
from pathlib import Path
from typing import Type

from codeline.exceptions import (PluginImplementationException,
                                 PluginNotFoundException)
from codeline.model.pluginmeta import PluginMeta
from codeline.sdk import CodelinePlugin
from codeline.util.error import catch

log = logging.getLogger(__name__)


class PluginService:
    """Functionality to load and handle plugins"""

    def __init__(self, plugin_directory: Path):
        """Load plugins on-startup"""
        super().__init__()
        log.debug(f'Loading plugins from {plugin_directory}')
        sys.path.insert(0, str(plugin_directory))
        loaded_plugins = self._load_all_plugins(plugin_directory)
        self._plugins = {plugin.trigger: plugin for plugin in loaded_plugins}
        for name, _ in self._plugins.items():
            log.debug(f'Loaded plugin: {name}')

    def get_plugin_for_trigger(self, trigger: str) -> PluginMeta:
        """Find the right plugin for a given command trigger"""
        plugin = self._plugins.get(trigger)
        if not plugin:
            raise PluginNotFoundException(trigger)

        return plugin

    @staticmethod
    def _load_plugin(plugin_path: Path) -> PluginMeta:
        """Load a plugin which is already on the path

        Args:
            plugin_name     The name of the plugin's main directory

        Returns:
            PluginMeta      An object describing the plugin, including a reference to its instance

        Raises:
            PluginImplementationException   The plugin cannot be loaded
        """
        plugin_name = plugin_path.stem
        entrypoint = '.'.join([plugin_name, 'main'])
        try:
            module = importlib.import_module(entrypoint)
        except ModuleNotFoundError as e:
            log.exception(e)
            raise PluginImplementationException(f'Plugin could not be loaded: {plugin_name}') from e

        klass: Type[CodelinePlugin] = getattr(module, 'Plugin', None)
        if not klass:
            raise PluginImplementationException(f"Could not load plugin: {plugin_name}")

        return PluginMeta(plugin_name, klass())

    def _load_all_plugins(self, directory: Path):
        """Finds all likely-plugins in the plugin directory and loads them"""
        is_plugin_dir = lambda dir_name: dir_name.suffix != '.py' and '__pycache__' not in str(dir_name)
        plugin_dirs = [plugin_dir for plugin_dir in directory.iterdir() if is_plugin_dir(plugin_dir)]
        loaded_plugins = [
            loaded_plugin for plugin in plugin_dirs
            if (loaded_plugin := catch(lambda: self._load_plugin(plugin), to_catch=PluginImplementationException))
            is not None
        ]

        return loaded_plugins
