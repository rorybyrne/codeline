"""Exceptions

Author: Rory Byrne <rory@rory.bio>
"""


class PluginImplementationException(Exception):
    """Raised when a plugin cannot be executed"""


class PluginNotFoundException(Exception):
    """Raised when a plugin cannot be loaded"""
