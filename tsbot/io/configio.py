#!/usr/python

import json
import os
from logging import getLogger

# get logger from parent
logger = getLogger(__name__)

# config file for settings relative to this file
config_path = os.path.join(os.path.dirname(__file__), "..", "tsbot.cfg")


def read_config():
    """
    Reads the config file, which containing different settings, from the previously set path.
    :return: returns config io as dictionary
    """

    try:
        with open(config_path) as json_data_file:
            data = json.load(json_data_file)
            return data

    except Exception as e:
        logger.exception("An error occurred while reading config file")


def write_config(data):
    """
    Writes the config file from the previously set path with the given io.
    :param data: io which should be stored in config file
    :return: None
    """
    try:
        with open(config_path) as json_data_file:
            json.dump(data, json_data_file)

    except Exception as e:
        logger.exception("An error occurred while writing config file")
