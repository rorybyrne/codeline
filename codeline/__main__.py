"""Entrypoint for Codeline

Author: Rory Byrne <rory@rory.bio>
"""

import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from dependency_injector.wiring import Provide, inject

from codeline.conf import Settings
from codeline.containers import Codeline
from codeline.oracle.oracle import Oracle
from codeline.service.command import CommandService
from codeline.util import log

logger = logging.getLogger(f'codeline.{__name__}')


def build_parser() -> ArgumentParser:
    """Parse arguments from command line"""
    parser = ArgumentParser("Codeline")
    parser.add_argument('--watch', nargs='?', const="all",  help="Watch a specific directory")
    parser.add_argument('--run', type=str, help="Run commands in a single file")

    return parser


def main():
    """Configure the launch the dependency injector

    If a file is passed in via argv, that will be run directly.
    """
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])

    settings = Settings.load()
    codeline = Codeline()
    codeline.config.from_dict(vars(settings))

    log_conf = codeline.config.log_conf()
    log.configure(log_conf)

    codeline.wire(modules=[sys.modules[__name__]])

    if args.run:
        run(Path(args.run).resolve())
    elif args.watch:
        if args.watch == "all":
            launch()
        else:
            watch(Path(args.watch).resolve())
    else:
        parser.print_help()


@inject
def watch(
    directory: Path,
    oracle: Oracle = Provide[Codeline.oracle]
):
    """Watch a specific directory"""
    if not directory.is_dir():
        print(f"This directory doesn't exist: {directory}")
        sys.exit(1)

    oracle.start(directory)


@inject
def run(
    file_path: Path,
    command_service: CommandService = Provide[Codeline.services.command_service]
):
    """Process a file directly"""
    if not file_path.is_file():
        print(f"This file doesn't exist: {file_path}")
        sys.exit(1)

    command_service.process_file(file_path)


@inject
def launch(oracle: Oracle = Provide[Codeline.oracle]):
    """Run the oracle to watch for changes"""
    try:
        oracle.start()
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
