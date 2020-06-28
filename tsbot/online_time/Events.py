#!/usr/bin/env python3

from logging import getLogger
from threading import Thread
from queue import Queue
from ts3.query import TS3TimeoutError
from time import time

# local imports
from tsbot.common.TsServer import TsServer
from tsbot.online_time.DbQuery import DbQuery as DBHandler
from tsbot.online_time.Worker import EventWorker
from tsbot.online_time.History import History

# Using global logger
logger = getLogger("main")


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

        logger.info("Event handling setup...")
        logger.debug("setting up ts query")
        self.ts = TsServer()

        # handler for events
        self.event_queue = Queue()
        history_queue = Queue()

        logger.debug("setting up event and history workers")
        event_worker = EventWorker(self.event_queue, history_queue)
        history_worker = History(history_queue)

        # Threading setup for the other event workers
        # object to inform threads of program exit
        logger.debug("setting up Threads")
        self._sentinel = object()
        self.event_worker_thread = Thread(target=event_worker.run, args=(self._sentinel,))
        self.event_worker_thread.start()
        logger.debug("thread for event worker started")

        self.history_worker_thread = Thread(target=history_worker.run, args=(self._sentinel,))
        self.history_worker_thread.start()
        logger.debug("thread for history worker started")
        logger.info("Event handling setup complete!")

    def handle_events(self):
        """
        Creates and listens for ts events. Queues the events for the appropriate sub-handler

        :return: None
        """

        logger.info("setup to handle events")
        self.init_active_clients()
        self.ts.exec_query("servernotifyregister", **{"event": "server"})

        while True:
            logger.info("sending keep alive signal")
            self.ts.keep_alive()
            try:
                logger.info("waiting for event...")
                event = self.ts.wait_for_event(120)
            except TS3TimeoutError:
                # when timeout send keep alive and wait again
                pass
            else:
                # event time for processing
                logger.info("processing new event")
                event[0]['event_time'] = int(time())
                logger.debug("adding event to event queue: {}".format(event))
                self.event_queue.put(event)

    def init_active_clients(self):
        # TODO: exclude gids und uuids from config
        """
        Will initialize the active_clients table with the already connected clients on the server

        :return: None
        """
        logger.info("Initializing online clients...")
        client_list = self.ts.exec_query("clientlist", "times", "uid", "groups", "info", "country")

        logger.debug("going through clients from clientlist")
        for client in client_list:
            # change key name for queryhandler
            client['join_time'] = client['client_lastconnected']
            # need client_description key
            client['client_description'] = ""

            logger.debug("inserting entry for client: <{}>".format(client))
            DBHandler.insert_db_entry("active_clients", **client)

    def run(self):
        """
        Main run method which will be executed when the online time will be counted

        :return:
        """

        try:
            logger.info("running main method")
            self.handle_events()
        finally:
            # puts sentinel when program is stopped to tell threads to quit
            logger.info("sending stop signal to threads")
            self.event_queue.put(self._sentinel)

            # waiting for threads to quit
            logger.info("waiting for threads to quit")
            self.event_worker_thread.join()
            logger.debug("event_worker thread was stopped")
            self.history_worker_thread.join()
            logger.debug("history_worker thread was stopped")




