#!/usr/python

import json
import logging

# get logger from parent
logger = logging.getLogger(__name__)

# config file for settings
config_path = "tsbot.cfg"


def read_config():
    """
    reads the config file, which containing different settings, from the previously set path
    :return: returns config data as dictionary
    """

    try:
        with open(config_path) as json_data_file:
            data = json.load(json_data_file)
            return data

    except Exception as e:
        logger.exception("An error occurred while reading config file")


def write_config(data):
    """
    writes the config file from the previously set path with the given data
    :param data: data which should be stored in config file
    :return: None
    """
    try:
        with open(config_path) as json_data_file:
            json.dump(data, json_data_file)

    except Exception as e:
        logger.exception("An error occurred while writing config file")
