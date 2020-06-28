#!/usr/bin/env python3

import logging
from logging.handlers import RotatingFileHandler
from os.path import join, dirname

# local imports
from tsbot.common.ConfigIo import ConfigIo as cio


class Log(object):

    def __init__(self):
        pass

    @staticmethod
    def init_logger():

        # TODO: Configure logger settings (with config options)
        # Configure logging

        logger_names = {"tsbot": "tsbot.log", "sql": "sql.log", "ts": "ts.log"}

        # TODO maybe add log file config
        logging_cfg = cio.read_config()["logging"]

        # TODO: different loggers for different components (database, ts, ...)
        handler = RotatingFileHandler(logging_path, maxBytes=1000000000, backupCount=3)
        log_format = "%(asctime)s::%(levelname)s::%(name)s::%(filename)s::%(lineno)d::%(message)s"

        # logger = getLogger("main")
        logger.setLevel(logging_cfg["level"])

        # get log path
        logging_path = {}
        for key in logger_names:
            logging_path[key] = join(dirname(__file__), "..", "logs", logger_names[key])

        # RotatingFileHandler to split logs

        #handler = FileHandler(logging_path)

        # use format
        formatter = Formatter(log_format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)


