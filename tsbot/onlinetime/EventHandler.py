#!/usr/python

from queue import Queue
import threading
import logging

from tsbot.onlinetime.JoinEventHandler import JoinEventHandler
from tsbot.onlinetime.LeaveEventHandler import LeaveEventHandler
from tsbot.io.TsServer import TsServer


class EventHandler(object):

    ts = None
    join_queue = None
    join_event_handler = None
    leave_queue = None
    leave_event_handler = None

    def __init__(self):
        # TODO: Configure logger settings (with config options)
        # Configure logging
        log_format = "%(asctime)s::%(levelname)s::%(name)s::" \
                     "%(filename)s::%(lineno)d::%(message)s"
        logging.basicConfig(filename='mylogs.log', level='DEBUG', format=log_format)

        self.ts = TsServer()

        # Event handler for joining events
        self.join_queue = Queue()
        self.join_event_handler = JoinEventHandler(self.join_queue)

        # Event handler for leaving events
        self.leave_queue = Queue()
        self.leave_event_handler = LeaveEventHandler(self.leave_queue)

        # TODO: Threads for handlers

    def join_event(self):
        # TODO
        pass

    def leave_event(self):
        # TODO
        pass

    def run(self):
        # TODO
        pass
