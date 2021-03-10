"""Service entrypoint

Author: Rory Byrne <rory@rory.bio>
"""
import logging

import sys
from dependency_injector.wiring import inject, Provide

from codeline.containers import Codeline
from codeline.oracle.oracle import Oracle
from codeline.util import log
from codeline.util.configure import configure

logger = logging.getLogger(__name__)


def main():
    codeline = Codeline()
    configure(codeline)
    log_conf = codeline.config.core.log_conf()
    log.configure(log_conf)
    codeline.wire(modules=[sys.modules[__name__]])

    try:
        launch()
    except Exception as e:
        logger.exception(e)


@inject
def launch(oracle: Oracle = Provide[Codeline.oracle]):
    logger.info("Launching Codeline...")
    oracle.start()


if __name__ == "__main__":
    main()
