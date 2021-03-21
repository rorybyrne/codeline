"""Configuration

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings():
    """Responsible for loading all settings from disk/defaults before starting the app

    Here, user-defined settings like custom templates can be loaded.
    """

    projects_file: Path
    plugin_directory: Path
    log_conf: Path

    default = {
        "projects_file": str(Path("~/.local/share/codeline/projects.json").resolve()),
        "plugin_directory": str(Path("~/.local/share/codeline/plugins").resolve()),
        "log_conf": str(Path(__file__, "../../log.conf").resolve())
    }

    development = {
        "projects_file": str(Path(__file__, "../../dev/projects.json").resolve()),
        "plugin_directory": str(Path(__file__, "../../plugins").resolve()),
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
    def _development() -> dict:
        """Return the development settings"""
        return Settings.development

    @staticmethod
    def load(debug: bool = False) -> "Settings":
        """Load the settings"""
        if debug:
            main_settings = Settings._development()
        else:
            main_settings = Settings._default()

        local_settings = Settings._from_local()
        project_settings = Settings._from_project()

        local_settings.update(project_settings)  # Roll project into local settings
        main_settings.update(local_settings)  # Roll both into the default settings

        settings = Settings(
            Path(main_settings["projects_file"]),
            Path(main_settings["plugin_directory"]),
            Path(main_settings["log_conf"]),
        )

        return settings
