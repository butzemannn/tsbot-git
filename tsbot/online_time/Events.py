#!/usr/bin/env python3

from logging import getLogger
from threading import Thread
from queue import Queue
from ts3.query import TS3TimeoutError
from time import time

# local imports
from tsbot.common.TsServer import TsServer
from tsbot.online_time.DbQuery import DbQuery
from tsbot.online_time.Worker import EventWorker
from tsbot.online_time.History import History

# choosing correct logger
logger = getLogger("tsbot.onlinetime")


class Events(object):
    """
    Listens on the ts3 server for events and queues joining as well as leaving events for the appropriate
    sub-handler.
    """

    # Attributes
    ts = None
    _sentinel = None

    event_queue = None
    event_worker_thread = None

    history_worker_thread = None

    def __init__(self):
        """
        Constructor which sets up the event_worker
        """

        logger.debug("Setting up ts query and workers")
        self.ts = TsServer()

        # handler for events
        self.event_queue = Queue()
        history_queue = Queue()

        event_worker = EventWorker(self.event_queue, history_queue)
        history_worker = History(history_queue)

        # Threading setup for the other event workers
        # object to inform threads of program exit
        self._sentinel = object()
        self.event_worker_thread = Thread(target=event_worker.run, args=(self._sentinel,))
        self.event_worker_thread.name = "WorkerThread"
        self.event_worker_thread.start()
        logger.debug("Thread for event worker started")

        self.history_worker_thread = Thread(target=history_worker.run, args=(self._sentinel,))
        self.history_worker_thread.name = "HistoryThread"
        self.history_worker_thread.start()
        logger.debug("Thread for history worker started")

    def handle_events(self):
        """
        Creates and listens for ts events. Queues the events for the appropriate sub-handler

        :return: None
        """

        logger.info("Setup to handle events")
        self.init_active_clients()
        self.ts.exec_query("servernotifyregister", **{"event": "server"})

        while True:
            self.ts.keep_alive()

            try:
                event = self.ts.wait_for_event(120)
            except TS3TimeoutError:
                # when timeout send keep alive and wait again
                pass
            else:
                # event time for processing
                logger.debug("Processing new event")
                event[0]['event_time'] = int(time())
                logger.debug("Adding event to event queue: {}".format(event))
                self.event_queue.put(event)

    def init_active_clients(self):
        # TODO: exclude gids und uuids from config
        """
        Will initialize the active_clients table with the already connected clients on the server

        :return: None
        """
        logger.info("Initializing online clients...")
        client_list = self.ts.exec_query("clientlist", "times", "uid", "groups", "info", "country")

        for client in client_list:
            # change key name for query handler
            client['join_time'] = client['client_lastconnected']
            # need client_description key
            client['client_description'] = ""

            logger.debug("Inserting entry for client: <{}>".format(client))
            DbQuery.insert_db_entry("active_clients", **client)

    def run(self):
        """
        Main run method which will be executed when the online time will be counted

        :return:
        """

        try:
            logger.info("Running main method")
            self.handle_events()
        finally:
            # puts sentinel when program is stopped to tell threads to quit
            logger.info("Sending stop signal to threads")
            self.event_queue.put(self._sentinel)

            # waiting for threads to quit
            logger.info("Waiting for threads to quit")
            self.event_worker_thread.join()
            self.history_worker_thread.join()
            logger.debug("Both threads were stopped")




