"""Oracle

@author Rory Byrne <rory@rory.bio>
"""

import logging
from pathlib import Path
from time import sleep
from typing import Dict, List

from watchdog.events import FileSystemEventHandler  # type: ignore
from watchdog.observers import Observer  # type: ignore
from watchdog.observers.api import ObservedWatch  # type: ignore

from codeline.oracle.handler.project import ProjectEventHandler
from codeline.oracle.handler.registry import RegistryEventHandler
from codeline.service.registry import RegistryService

log = logging.getLogger(__name__)


class Oracle:
    """Monitor active projects and the project registry"""

    def __init__(self, registry_service: RegistryService, observer: Observer,
                 project_event_handler: ProjectEventHandler,
                 registry_event_handler: RegistryEventHandler):
        super().__init__()
        assert registry_service, "Project service missing"
        assert observer, "Observer missing"
        self._registry_service = registry_service
        self._observer = observer
        self._projects_file = self._registry_service.projects_file

        self._watches_by_dir: Dict[str, ObservedWatch] = dict()

        # Handlers
        self._project_event_handler = project_event_handler
        self._registry_event_handler = registry_event_handler
        self._registry_event_handler.set_handler(self._reconcile)

    def start(self, project_dir: Path = None):
        """Monitor the projects file and any registered projects"""
        if project_dir:
            self.watch(str(project_dir), self._project_event_handler, recursive=True)
            self._start()
        else:
            if not self._projects_file.is_file():
                raise FileNotFoundError(f"Projects file does not exist: {self._projects_file}")

            # Watch the plan_home directory
            self.watch(self._projects_file, self._registry_event_handler, recursive=False)

            # Watch the registered workspaces
            projects = self._registry_service.load_projects()
            if len(projects) == 0:
                log.debug("No projects found.")
            else:
                for project in projects:
                    self.watch(
                        project.root_dir, self._project_event_handler, recursive=True
                    )

            self._start()

    def _start(self):
        self._observer.start()
        # Loop
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
        self._observer.join()

    def watch(self, directory: str, handler: FileSystemEventHandler, recursive=False):
        """Watch a project directory with the given handler"""
        watch = self._observer.schedule(handler, directory, recursive=recursive)
        self._watches_by_dir[directory] = watch

        log.debug(f"Watched {directory}")

    def unwatch(self, workspace: str):
        """Unwatch a project"""
        watch = self._watches_by_dir[workspace]
        self._observer.unschedule(watch)
        del self._watches_by_dir[workspace]

    def _reconcile(self, project_dirs: List[str]):
        """Watch any new projects, and unwatch any which have been removed"""
        watched_projects = [d for d in self._watched_paths if d != self._projects_file]
        for project in project_dirs:
            if project not in watched_projects:
                self.watch(project, self._project_event_handler, recursive=True)

        for watched_project in watched_projects:
            if watched_project not in project_dirs:
                to_remove = watched_project
                self.unwatch(to_remove)
                log.debug(f"Unwatched {to_remove}")

    @property
    def _watched_paths(self):
        return self._watches_by_dir.keys()
