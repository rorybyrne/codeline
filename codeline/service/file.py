"""File service

Author: Rory Byrne <rory@rory.bio>
"""
import os

from codeline.model.file import File
from codeline.util.log import Logger


class FileService(Logger):

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def read(file_path: str) -> File:
        if not FileService.is_file(file_path):
            raise RuntimeError(f"{file_path} is not a file.")

        with open(file_path) as f:
            lines = f.readlines()

            return File.from_lines(file_path, lines)
