#!/usr/bin/env python3

from logging import getLogger
from sys import exit

# local imports
from tsbot.common.TsServer import TsServer

logger = getLogger("tsbot.onlinetime")


class History(object):

    _sentinel = None
    history_queue = None

    def __init__(self, event_queue):
        self.history_queue = event_queue

    def add_history_entry(self, data: dict):
        pass

    def run(self, _sentinel):
        # TODO description
        self._sentinel = _sentinel

        while True:
            data = self.history_queue.get()

            if data is self._sentinel:
                exit()

            # has to get some extra information
            ts = TsServer()
            db_data = ts.exec_query("clientdbinfo", {"cldbid": data["client_database_id"]})
            # create copy for thread safety
            hist_event = dict(data)
            hist_event.update(db_data)

            self.add_history_entry(data)

