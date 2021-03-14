"""Plugin Result

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass


@dataclass
class Result:
    """The final outcome of your plugin's execution"""
    successful: bool
    message: str
