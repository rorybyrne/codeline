"""Service entrypoint

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

logger = logging.getLogger(__name__)


def main():
    codeline = Codeline()
    configure(codeline, debug=True)
    log_conf = codeline.config.core.log_conf()
    log.configure(log_conf)
    codeline.wire(modules=[sys.modules[__name__]])

    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            launch_direct(file_path)
        else:
            launch()
    except Exception:
        # logger.exception(e)
        raise


@inject
def launch_direct(
    file_path: str,
    command_service: CommandService = Provide[Codeline.services.command_service]
):
    command_service.process_file(file_path)


@inject
def launch(oracle: Oracle = Provide[Codeline.oracle]):
    logger.info("Launching Codeline...")
    oracle.start()


if __name__ == "__main__":
    main()
