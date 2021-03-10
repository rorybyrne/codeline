"""Configuration

Author: Rory Byrne <rory@rory.bio>
"""
import os
from pathlib import Path

from codeline.containers import Codeline

HOME = str(Path.home())
DEBUG = os.environ.get('CL_DEBUG')

if DEBUG:
    CONFIG_DIR = './dev'
else:
    CONFIG_DIR = os.path.join(HOME, ".local", "share", "codeline")


def configure(codeline: Codeline):
    config_filename = 'config-debug.yaml' if DEBUG else 'config.yaml'
    config_file = os.path.join(CONFIG_DIR, config_filename)
    if not os.path.exists(config_file):
        raise RuntimeError(f'Config file not found at "{config_file}"')

    codeline.config.from_yaml(config_file)
    projects_file = codeline.config.core.projects_file().replace("$HOME", HOME)
    codeline.config.set("core.projects_file", projects_file)

    log_conf = codeline.config.core.log_conf().replace("$HOME", HOME)
    codeline.config.set("core.log_conf", log_conf)
