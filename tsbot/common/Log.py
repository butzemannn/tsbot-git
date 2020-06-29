#!/usr/bin/env python3

import logging
from logging.handlers import RotatingFileHandler
from os.path import join, dirname

# local imports
from tsbot.common.ConfigIo import ConfigIo as cio


class Log(object):

    @staticmethod
    def init_logger():

        # Configure logging
        # TODO maybe add log file config as ini file
        # logging_cfg = cio.read_config()["logging"]
        logging_level = "DEBUG"

        # logging names and file paths
        sub_logger_names = {"onlinetime": "onlinetime.log", "sql": "sql.log", "ts": "ts.log", "tests": "tests.log"}

        log_format = "%(asctime)s::%(levelname)s::%(filename)s::%(threadName)s::%(funcName)s:: %(message)s"
        formatter = logging.Formatter(log_format)

        # top level logger setup
        logging_path = join(dirname(__file__), "..", "logs", "tsbot.log")
        top_handler = RotatingFileHandler(logging_path, maxBytes=2000000000, backupCount=3)
        top_handler.setFormatter(formatter)

        # different loggers for
        top_logger = logging.getLogger("tsbot")
        top_logger.setLevel(logging_level)
        top_logger.addHandler(top_handler)

        # settings for different sub logging
        logging_path = {}
        for key in sub_logger_names:
            logging_path[key] = join(dirname(__file__), "..", "logs", sub_logger_names[key])
            # RotatingFileHandler to split logs
            handler = RotatingFileHandler(logging_path[key], maxBytes=2000000000, backupCount=3)
            handler.setFormatter(formatter)

            # different loggers for
            logger = logging.getLogger("tsbot.{}".format(key))
            logger.setLevel(logging_level)
            logger.addHandler(handler)
