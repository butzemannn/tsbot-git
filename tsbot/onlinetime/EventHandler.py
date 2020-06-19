#!/usr/python

import logging
from threading import Thread
from queue import Queue
from ts3.query import TS3TimeoutError
from time import time

# local imports
from tsbot.onlinetime.EventWorker import EventWorker
from tsbot.io.TsServer import TsServer


class EventHandler(object):
    """
    Listens on the ts3 server for events and queues joining as well as leaving events for the appropriate
    sub-handler.
    """

    # Attributes
    ts = None
    _sentinel = None

    event_queue = None
    event_worker = None
    event_worker_thread = None

    def __init__(self):
        """
        Constructor which sets up the event_worker and the leave_event_handler
        """
        # TODO: Configure logger settings (with config options)
        # Configure logging
        log_format = "%(asctime)s::%(levelname)s::%(name)s::" \
                     "%(filename)s::%(lineno)d::%(message)s"
        logging.basicConfig(filename='mylogs.log', level='DEBUG', format=log_format)

        self.ts = TsServer()

        # Event handler for joining events
        self.event_queue = Queue()
        self.event_worker = EventWorker(self.event_queue)

        # Threading setup for the other event workers
        # object to inform threads of program exit
        self._sentinel = object()
        self.event_worker_thread = Thread(target=self.event_worker.run, args=(self._sentinel,))
        self.event_worker_thread.start()

    def handle_events(self):
        """
        Creates and listens for ts events. Queues the events for the appropriate sub-handler when detected according
        to the reasonid
        :return: None
        """

        self.ts.exec_query("servernotifyregister", {"event": "server"})
        while True:
            self.ts.keep_alive()
            try:
                event = self.ts.wait_for_event(120)
            except TS3TimeoutError:
                # when timeout send keep alive and wait again
                pass
            else:
                # add event to queue for worker
                event[0]['event_time'] = int(time())
                self.event_queue.put(event)

    def init_active_clients(self):
        """
        Will initialize the active_clients table with the already connected clients on the server
        :return: None
        """
    def run(self):
        """
        Main run method which will be executed when the online time will be counted
        :return:
        """
        try:
            self.handle_events()

        finally:
            # puts sentinel when program is stopped to tell threads to quit
            self.event_queue.put(self._sentinel)

            # waits for threads to quit
            self.event_worker_thread.join()




