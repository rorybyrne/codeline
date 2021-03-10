"""Project model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass


@dataclass
class Project:
    root_dir: str
