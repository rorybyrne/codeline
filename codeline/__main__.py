"""Entrypoint for Codeline

Author: Rory Byrne <rory@rory.bio>
"""

import logging
import os
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from dependency_injector.wiring import Provide, inject

from codeline.conf import Settings
from codeline.containers import Codeline
from codeline.oracle.oracle import Oracle
from codeline.service.command import CommandService
from codeline.util import log

logger = logging.getLogger(f'codeline.{__name__}')
DEBUG = os.environ.get('CL_DEBUG')


def parse_args() -> Namespace:
    """Parse arguments from command line"""
    parser = ArgumentParser("Codeline")
    parser.add_argument('--watch', type=str)
    parser.add_argument('--run', type=str)

    return parser.parse_args(sys.argv[1:])


def main():
    """Configure the launch the dependency injector

    If a file is passed in via argv, that will be run directly.
    """
    args = parse_args()

    settings = Settings.load(debug=DEBUG)
    codeline = Codeline()
    codeline.config.from_dict(vars(settings))

    log_conf = codeline.config.log_conf()
    log.configure(log_conf)

    logger.info("Launching Codeline...")
    codeline.wire(modules=[sys.modules[__name__]])

    if args.run:
        run(Path(args.run).resolve())
    elif args.watch:
        watch(Path(args.watch).resolve())
    else:
        launch()


@inject
def watch(
    directory: Path,
    oracle: Oracle = Provide[Codeline.oracle]
):
    """Watch a specific directory"""
    oracle.start(directory)


@inject
def run(
    file_path: Path,
    command_service: CommandService = Provide[Codeline.services.command_service]
):
    """Process a file directly"""
    command_service.process_file(file_path)


@inject
def launch(oracle: Oracle = Provide[Codeline.oracle]):
    """Run the oracle to watch for changes"""
    oracle.start()


if __name__ == "__main__":
    main()
