"""Logging

Author: Rory Byrne <rory@rory.bio>
"""
import logging
import logging.config


def configure(config_file: str):
    """Configure logging from a file"""
    logging.config.fileConfig(fname=config_file)
