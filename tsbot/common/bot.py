#!/usr/python

import logging

class bot():

    def __init__(self):
        """
        setting up different base data like logging settings, ts3 connection etc.
        """

        # Configure logging
        log_format = "%(asctime)s::%(levelname)s::%(name)s::" \
                     "%(filename)s::%(lineno)d::%(message)s"
        logging.basicConfig(filename='mylogs.log', level='DEBUG', format=log_format)
