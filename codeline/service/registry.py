"""Registry service

Author: Rory Byrne <rory@rory.bio>
"""
import json
import logging
import os
from typing import List

from codeline.model.project import Project

log = logging.getLogger(__name__)


class RegistryService:
    """Registry for the user's active projects

    Projects are not monitored by default. To enable Codeline for a project,
    you must run `codeline activate <src_dir>` in the root directory of the project.
    """

    def __init__(self, projects_file: str):
        super().__init__()
        assert projects_file, "Projects filename missing"
        self._projects_file = projects_file

    def load_projects(self) -> List[Project]:
        """Load the projects from the projects file"""
        projects = self._load_projects()

        return projects

    def register(self, project: Project):
        """Registers the project to be monitored by Codeline

        Args:
            project:    The project to be registered
        """
        project_registered = self._project_is_registered(project)

        if project_registered:
            log.debug(f'Project already registered: {project}')
            return
        else:
            self._register(project)

    @property
    def directory(self):
        return os.path.dirname(self._projects_file)

    # Private ###

    def _register(self, project: Project):
        """Performs the registration"""
        self._save_project(project)

    def _project_is_registered(self, project: Project):
        """Checks if the project exists among the existing saved projects"""
        projects = self._load_projects()
        return any(pj for pj in projects if pj.root_dir == project.root_dir)

    def _save_project(self, project: Project):
        """Saves the project to the project file"""
        projects = self._load_projects()
        if self._project_is_registered(project):
            raise RuntimeError("Project already exists")
        else:
            projects.append(project)
            self._save_projects(projects)

    def _load_projects(self) -> List[Project]:
        """Loads registered projects from the projects file"""
        try:
            with open(self._projects_file, "r") as f:
                projects_data: dict = json.load(f)

                if (projects := projects_data.get("projects")) is None or not isinstance(projects, list):
                    raise RuntimeError(f"Invalid projects file: {self._projects_file}")

                return [Project(pj) for pj in projects]
        except FileNotFoundError:
            raise RuntimeError(f"Could not find projects file: {self._projects_file}")

    def _save_projects(self, projects: List[Project]):
        """Saves the list of projects, overwriting the current file"""
        try:
            with open(self._projects_file, "r+") as f:
                projects_data: dict = json.load(f)
                if not (_projects := projects_data.get("projects")) or not isinstance(_projects, list):
                    raise RuntimeError(f"Invalid projects file: {self._projects_file}")

                projects_data["projects"] = [pj.root_dir for pj in projects]

                f.seek(0)
                json.dump(projects_data, f)
                f.truncate()
        except FileNotFoundError:
            raise RuntimeError(f"Could not find projects file: {self._projects_file}")
