"""Entrypoint for Codeline

Author: Rory Byrne <rory@rory.bio>
"""
import logging
import sys

from dependency_injector.wiring import Provide, inject

from codeline.containers import Codeline
from codeline.oracle.oracle import Oracle
from codeline.service.command import CommandService
from codeline.util import log
from codeline.util.configure import configure

logger = logging.getLogger(f'codeline.{__name__}')


def main():
    """Configure the launch the dependency injector

    If a file is passed in via argv, that will be run directly.
    """
    codeline = Codeline()  # sup
    configure(codeline, debug=True)
    log_conf = codeline.config.core.log_conf()
    log.configure(log_conf)

    logger.info("Launching Codeline...")
    codeline.wire(modules=[sys.modules[__name__]])

    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            launch_direct(file_path)
        else:
            launch()
    except Exception as e:
        logger.exception(e)


@inject
def launch_direct(
    file_path: str,
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
