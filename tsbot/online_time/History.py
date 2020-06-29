#!/usr/bin/env python3

from logging import getLogger
from sys import exit

# local imports
from tsbot.common.TsServer import TsServer
from tsbot.online_time.DbQuery import DbQuery

logger = getLogger("tsbot.onlinetime")


class History(object):

    _sentinel = None
    history_queue = None

    def __init__(self, event_queue):
        self.history_queue = event_queue

    def add_history_entry(self, data: dict):

        data['online_time'] = data['leave_time'] - data['join_time']
        DbQuery.insert_db_entry("client_history", **data)

    def run(self, _sentinel):
        # TODO description
        self._sentinel = _sentinel

        while True:
            # waiting for event in queue
            data = self.history_queue.get()

            if data is self._sentinel:
                exit()

            # has to get some extra information
            with TsServer() as ts:
                db_data = ts.exec_query("clientdbinfo", **{"cldbid": data["client_database_id"]})[0]

            # create copy for thread safety
            hist_event = dict(data)
            client_history_data = {**hist_event, **db_data}

            self.add_history_entry(client_history_data)

