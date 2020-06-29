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
        while True:
            ts = TsServer()
            client_list = ts.exec_query("clientlist", "times")

            for client in client_list:
                # TODO make afk time configurable in cfg
                if client_list['client_idle_time'] >= 1800:
                    try:
                        DbQuery.update_afk_time()

                    except Exception as e:
                        pass

            sleep(600)

    def run(self):
        pass
