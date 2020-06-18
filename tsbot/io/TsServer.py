#!/usr/python

import logging
import ts3

from tsbot.io.configio import read_config

logger = logging.getLogger(__name__)


class TsServer(object):

    # reading ts3 credentials from config file
    ts3_credentials = read_config()["ts3"]
    ts3conn = None

    def __init__(self):
        """
        Initializes the ssh connection to the ts3 server.
        """

        # query url setup with ssh as protocol
        URL = "ssh://{user}:{password}@{host}:{port}".format(**self.ts3_credentials)
        try:
            # establishing the connection to the ts server
            self.ts3conn = ts3.query.TS3ServerConnection(URL)
            self.ts3conn.exec_("use", sid=self.ts3_credentials["serverid"])

        except Exception as e:
            logger.exception("Connecting to the ts3 server failed!")

    def exec_query(self, query: str, params: dict = None):
        """
        Executes a ts query command with the command 'query' and the parameters 'params'.
        The parameter dictionary keys must be named according to the command syntax found in the ts3 query manual.
        :param query: the query command given as string, e.g. "clientlist" or "clientpoke" according to the query manual
        :param params: a dictionary with query parameters with dict-keys named according to query manual,
                       e.g. {sid=1, clid=44, msg="Hello World"}
        :return: returns the query answer of the server
        """

        try:
            # execute correct query even when no parameters are needed
            if params:
                out = self.ts3conn.exec_(query, **params)
            else:
                out = self.ts3conn.exec_(query)
            # returns query response
            return out

        except Exception as e:
            logger.exception("An error occurred while executing the ts3 query!")
            self.ts3conn.close()

    def keep_alive(self):
        """
        Sends keep alive signal so the connection stays active.
        :return: None
        """
        self.ts3conn.send_keepalive()

    def close_connection(self):
        """
        Closes connection to the ts3 query.
        :return: None
        """
        self.ts3conn.close()




