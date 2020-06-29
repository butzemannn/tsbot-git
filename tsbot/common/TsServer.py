#!/usr/bin/env python3

import ts3
from logging import getLogger

# local imports
from tsbot.common.ConfigIo import ConfigIo as cio

logger = getLogger("tsbot.ts")


class TsServer(object):

    # reading ts3 credentials from config file
    ts3_credentials = cio.read_config()["ts3"]
    ts3conn = None

    def __init__(self):
        """
        Initializes the ssh connection to the ts3 server.
        """
        logger.info("Establishing new query connection to the ts server")

        # query url setup with ssh as protocol
        url = "ssh://{user}:{password}@{host}:{port}".format(**self.ts3_credentials)
        logger.debug("Connection url: ssh://{user}:***@{host}:{port}".format(**self.ts3_credentials))

        try:
            # establishing the connection to the ts server
            self.ts3conn = ts3.query.TS3ServerConnection(url)
            self.ts3conn.exec_("use", sid=self.ts3_credentials["serverid"])
            logger.debug("Using sid: {sid}", self.ts3_credentials)

            try:
                self.ts3conn.exec_("clientupdate", client_nickname="Hauseigener Bot")
                logger.debug("Ts connection established. Nickname: Hauseigener Bot")

            except ts3.query.TS3QueryError as e:
                # when username is already taken
                logger.debug("Nickname already taken. Not switching")

        except Exception as e:
            logger.exception("Connecting to the ts3 server failed!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def exec_query(self, query: str, *options, **params: dict):
        """
        Executes a ts query command with the command 'query' and the parameters 'params'.
        The parameter dictionary keys must be named according to the command syntax found in the ts3 query manual.

        :param query:
            the query command given as string, e.g. "clientlist" or "clientpoke" according to the query manual
        :param options:
            all initial options which are added with a '-',
            e.g. [times, uid, groups]
        :param params:
            a dictionary with query parameters with dict-keys named according to query manual,
            e.g. {sid=1, identifier=44, msg="Hello World"}

        :return:
            returns the query answer of the server
        """

        logger.debug("Executing query command: " + query + " " + str(options) + " " + str(params))

        try:
            # execute correct query even when no parameters are needed
            out = self.ts3conn.exec_(query, *options, **params)
            logger.debug("Command execution successful: " + str(out))
            return out

        except Exception as e:
            logger.exception("An error occurred while executing the ts3 query!")
            self.ts3conn.close()

    def keep_alive(self):
        """
        Sends keep alive signal so the connection stays active.

        :return: None
        """
        logger.debug("Sending keep alive signal")
        self.ts3conn.send_keepalive()

    def wait_for_event(self, timeout: int):
        """
        Holds the program and waits for an previously registered event

        :param timeout:
            is 0 when no timeout is specified

        :return:
            returns the event
        """

        logger.debug("Waiting for ts event...")
        return self.ts3conn.wait_for_event(timeout=timeout)

    def close(self):
        """
        Closes connection to the ts3 query.

        :return: None
        """

        self.ts3conn.close()
        logger.info("Closed the ts connection")






