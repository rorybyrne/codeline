"""Plugin Result

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass


@dataclass
class Result:
    successful: bool
    message: str
