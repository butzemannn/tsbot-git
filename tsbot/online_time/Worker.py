#!/usr/bin/env python3

from sys import exit
from time import time
from logging import getLogger

# local imports
from tsbot.online_time.DbQuery import DbQuery as DBHandler
from tsbot.common.ConfigIo import ConfigIo as cio

# get logger from parent
logger = getLogger(__name__)

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
        active_client_data = DBHandler.get_db_entry('active_clients', event[0]['clid'])
        DBHandler.delete_entry_from_clid('active_clients', event[0])

        # long term client data
        online_time_data = DBHandler.get_db_entry("online_time", active_client_data['client_unique_identifier'])

        return active_client_data, online_time_data

    @staticmethod
    def clear_temp_data():
        """
        Clears temporary data including the active_clients table

        :return: None
        """

        # Clears table of active_clients
        DBHandler.clear_table("active_clients")

    def join_event(self, event):
        """
        Accesses table and creates new user from a joining event

        :param event:
            the join event the user will be created from

        :return: None
        """
        event[0]['join_time'] = event[0]['event_time']
        DBHandler.insert_db_entry("active_clients", **event[0])

    def leave_event(self, event):
        """
        Calculates the online time and writes to table

        :param event:

        :return:
        """

        [active_client_data, online_time_data] = self._client_data_from_event(event)
        leave_time = int(time())

        # Setup for History Worker
        active_client_data['client_leave'] = leave_time
        self.history_queue.put(active_client_data)

        # check if user is excluded
        excluded_groups = cio.read_config()['onlinetime']['excluded_server_groups']
        excluded_user = cio.read_config()['onlinetime']['excluded_client_unique_identifier']

        if active_client_data['client_unique_identifier'] in excluded_user:
            return
        for groupid in active_client_data['client_servergroups'].split(","):
            if groupid in excluded_groups:
                return

        # check if user already exists
        if online_time_data:
            # calculate the current online time
            online_time_new = online_time_data['online_time'] + (leave_time - active_client_data['join_time'])
            online_time_data['online_time'] = online_time_new
            DBHandler.update_online_time_entry(**online_time_data)

        else:
            # create client when not already in table
            online_time_new = leave_time - active_client_data['join_time']
            active_client_data['online_time'] = online_time_new
            DBHandler.insert_db_entry('online_time', **active_client_data)

        DBHandler.delete_entry_from_clid("active_clients", active_client_data['clid'])

    def run(self, _sentinel: object):
        """
        Main run method which will be executed in the thread.

        :param _sentinel:
            object which will be queued when program got stopped

        :return: None
        """

        while True:
            # wait for new item in queue
            event = self.event_queue.get()

            # check if thread must be stopped
            if event is _sentinel:
                # clear all temp data
                self.clear_temp_data()
                self.history_queue.put(_sentinel)
                exit()

            # check if client joined or left the server
            reasonid = int(event[0]["reasonid"])

            # id 0: user joined the server
            if reasonid == 0:
                self.join_event(event)

            # id 3: timeout, 5: kick, 6: ban, 8: left, 11: server shutdown
            elif reasonid in [3, 5, 6, 8, 11]:
                self.leave_event(event)
                pass


