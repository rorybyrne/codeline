"""Project model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass


@dataclass
class Project:
    """A project in which the coder is working"""
    root_dir: str
