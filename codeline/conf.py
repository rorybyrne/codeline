"""Configuration

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Settings():
    """Responsible for loading all settings from disk/defaults before starting the app

    Here, user-defined settings like custom templates can be loaded.
    """

    projects_file: Path
    plugin_directories: List[Path]
    log_conf: Path

    default = {
        "projects_file": str(Path("~/.local/share/codeline/projects.json").expanduser()),
        "plugin_directories": [
            str(Path("~/.local/share/codeline/plugins").expanduser()),
            str(Path(__file__, "../../plugins").resolve())
        ],
        "log_conf": str(Path(__file__, "../../log.conf").resolve())
    }

    # Builders ##################################

    @staticmethod
    def _from_project() -> dict:
        """Attempt to load a config.yaml from the local git repository"""
        return {}

    @staticmethod
    def _from_local() -> dict:
        """Attempt to load a config.yaml from a default directory"""
        return {}

    @staticmethod
    def _default() -> dict:
        """Return the default settings"""
        return Settings.default

    @staticmethod
    def load() -> "Settings":
        """Load the settings"""
        main_settings = Settings._default()
        plugin_dirs = main_settings["plugin_directories"]

        local_settings = Settings._from_local()
        project_settings = Settings._from_project()

        local_settings.update(project_settings)  # Roll project into local settings
        main_settings.update(local_settings)  # Roll both into the default settings

        settings = Settings(
            Path(main_settings["projects_file"]),
            [Path(directory) for directory in plugin_dirs],
            Path(main_settings["log_conf"]),
        )

        return settings
