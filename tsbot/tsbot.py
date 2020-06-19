#!/usr/python

import logging
from tsbot.onlinetime.EventHandler import EventHandler

# local imports


def run_online_time():
    handler = EventHandler()
    handler.run()


def run():
    run_online_time()
