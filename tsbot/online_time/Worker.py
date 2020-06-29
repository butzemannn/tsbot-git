#!/usr/bin/env python3

from sys import exit
from time import time
from logging import getLogger

# local imports
from tsbot.online_time.DbQuery import DbQuery
from tsbot.common.ConfigIo import ConfigIo as cio

# get logger from parent
logger = getLogger("tsbot.onlinetime")

# TODO logging


class EventWorker(object):

    event_queue = None
    history_queue = None

    def __init__(self, event_queue, history_queue):
        """

        :param event_queue:
        """
        self.event_queue = event_queue
        self.history_queue = history_queue

    @staticmethod
    def _client_data_from_event(event):
        """
        Fetches the needed client data from active_clients and online_time tables from the given event.

        :param event:
            The ts3 event from which the data will be collected
        :return:
            Both table entries as dictionarys
        """

        # get client information from table and delete entry
        logger.debug("Fetching client data from event: " + str(event[0]))
        active_client_data = DbQuery.get_db_entry('active_clients', event[0]['clid'])

        # long term client data
        online_time_data = DbQuery.get_db_entry("online_time", active_client_data['client_unique_identifier'])

        logger.debug("Returning active_client_data and online_time_data: [{}], \n [{}]".format(str(active_client_data), str(online_time_data)))
        return active_client_data, online_time_data

    @staticmethod
    def clear_temp_data():
        """
        Clears temporary data including the active_clients table

        :return: None
        """

        # Clears table of active_clients
        logger.info("Clearing all temp data")
        DbQuery.clear_table("active_clients")

    def join_event(self, event):
        """
        Accesses table and creates new user from a joining event

        :param event:
            the join event the user will be created from

        :return: None
        """

        logger.info("Processing join event")
        event[0]['join_time'] = event[0]['event_time']
        logger.debug("Inserting joined client into the active_clients_table")
        DbQuery.insert_db_entry("active_clients", **event[0])

    def leave_event(self, event):
        """
        Calculates the online time and writes to table

        :param event:

        :return:
        """
        logger.info("Processing leave event")
        logger.debug("Fetching needed client data for processing")
        [active_client_data, online_time_data] = self._client_data_from_event(event)
        leave_time = int(time())

        # Setup for History Worker
        active_client_data['client_leave'] = leave_time
        logger.debug("Adding to client to history queue: [{}]".format(str(active_client_data)))
        self.history_queue.put(active_client_data)

        # check if user is excluded
        excluded_groups = cio.read_config()['onlinetime']['excluded_server_groups']
        excluded_user = cio.read_config()['onlinetime']['excluded_client_unique_identifier']

        if active_client_data['client_unique_identifier'] in excluded_user:
            logger.debug("Client is excluded user: [{}]".format(active_client_data['client_unique_identifier']))
            return

        for groupid in active_client_data['client_servergroups'].split(","):
            if groupid in excluded_groups:
                logger.debug("Client in excluded group: [{}]".format(groupid))
                return

        # check if user already exists
        if online_time_data:
            # calculate the current online time
            online_time_new = online_time_data['online_time'] + (leave_time - active_client_data['join_time'])
            online_time_data['online_time'] = online_time_new
            logger.debug("Updating user time in existing database entry: [{}]".format(str(online_time_data)))
            DbQuery.update_online_time_entry(**online_time_data)

        else:
            # create client when not already in table
            online_time_new = leave_time - active_client_data['join_time']
            active_client_data['online_time'] = online_time_new
            logger.debug("Creating user database entry: [{}]".format(str(online_time_data)))
            DbQuery.insert_db_entry('online_time', **active_client_data)

        DbQuery.delete_entry_from_clid("active_clients", active_client_data['clid'])

    def run(self, _sentinel: object):
        """
        Main run method which will be executed in the thread.

        :param _sentinel:
            object which will be queued when program got stopped

        :return: None
        """

        while True:
            # wait for new item in queue
            logger.debug("Waiting for new event in queue")
            event = self.event_queue.get()

            # check if thread must be stopped
            if event is _sentinel:
                # clear all temp data
                self.clear_temp_data()
                self.history_queue.put(_sentinel)
                logger.debug("Event is sentinel. Stopping...")
                exit()

            # check if client joined or left the server
            logger.debug("Working on new event [{}]".format(str(event[0])))
            reasonid = int(event[0]["reasonid"])

            # id 0: user joined the server
            if reasonid == 0:
                self.join_event(event)

            # id 3: timeout, 5: kick, 6: ban, 8: left, 11: server shutdown
            elif reasonid in [3, 5, 6, 8, 11]:
                self.leave_event(event)
                pass


