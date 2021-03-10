"""Logging

Author: Rory Byrne <rory@rory.bio>
"""
import logging
import logging.config


def configure(config_file: str):
    logging.config.fileConfig(fname=config_file)


class Logger:

    def __init__(self):
        self.log = logging.getLogger(f'codeline.{self.__class__.__name__}')
