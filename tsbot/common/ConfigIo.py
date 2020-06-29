#!/usr/bin/env python3

import json
import os
from logging import getLogger

# get logger from parent
logger = getLogger("tsbot")

# config file for settings relative to this file
config_path = os.path.join(os.path.dirname(__file__), "..", "tsbot.cfg")


class ConfigIo(object):

    @staticmethod
    def read_config():
        """
        Reads the config file, which containing different settings, from the previously set path.

        :return: returns config common as dictionary
        """

        logger.info("Reading config file")
        try:
            with open(config_path) as json_data_file:
                data = json.load(json_data_file)
                logger.debug("Reading config file was successful: " + str(data))
                return data

        except OSError:
            logger.exception("While opening the file an OS Error occurred")

        except ValueError:
            logger.exception("Decoding the JSON file has failed")

        except Exception as e:
            logger.exception("An error occurred while reading config file")

    @staticmethod
    def write_config(data):
        """
        Writes the config file from the previously set path with the given common.

        :param data:
            common which should be stored in config file

        :return: None
        """
        logger.info("Writing config file")

        try:
            with open(config_path) as json_data_file:
                json.dump(data, json_data_file)
                logger.debug("Writing the config file was successful: " + str(data))

        except OSError:
            logger.exception("While opening the file an OS Error occurred")

        except Exception as e:
            logger.exception("An error occurred while writing config file")
