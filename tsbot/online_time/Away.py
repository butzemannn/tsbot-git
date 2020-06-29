#!/usr/bin/env python3

from time import sleep
from logging import getLogger

# local imports
from tsbot.common.TsServer import TsServer
from tsbot.online_time.DbQuery import DbQuery

logger = getLogger("tsbot.onlinetime")


class Away(object):

    # TODO add logging
    def __init__(self):
        pass

    def log_afk_time(self):
        # TODO description
        # TODO stop condition (_sentinel)
        with TsServer() as ts:
            client_list = ts.exec_query("clientlist", "times")

        for client in client_list:
            # TODO make afk time configurable in cfg
            if client['client_idle_time'] >= 180:
                try:
                    DbQuery.update_afk_time(**client)

                except Exception as e:
                    pass

    def run(self):
        while True:
            self.log_afk_time()
            sleep(600)
