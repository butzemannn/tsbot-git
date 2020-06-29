#!/usr/bin/env python3

from logging import getLogger

# local imports
from tsbot.common.Log import Log
from tsbot.online_time.Events import Events


def run_online_time():
    handler = Events()
    handler.run()


def run():
    # setup logger
    Log.init_logger()
    _logger = getLogger("tsbot")
    _logger.info("Starting tsbot")
    try:
        run_online_time()
    except KeyboardInterrupt  as e:
        _logger.info("The running program has been interrupted manually.")
    except Exception as e:
        _logger.exception("An error occured \n")

    _logger.info("The program has finished. \n")
