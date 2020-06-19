#!/usr/python

from sys import exit
from time import time
from logging import getLogger

# local imports
from tsbot.io.database import exec_query

# get logger from parent
logger = getLogger(__name__)


class EventWorker(object):

    event_queue = None

    def __init__(self, event_queue):
        """

        :param event_queue:
        """
        self.event_queue = event_queue

    def join_event(self, event):
        """
        Accesses database and creates new user from a joining event
        :param event: the join event the user will be created from
        :return: None
        """
        # TODO: set correct variable types in query and in table
        query = "INSERT INTO active_clients (client_nickname, client_unique_identifier, client_database_id, clid, join_time) " \
                "VALUES ('{client_nickname}', '{client_unique_identifier}', {client_database_id}, {clid}, {join_time});".format(**event[0], join_time=event[0]['event_time'])
        exec_query(query)

    def leave_event(self, event):
        """
        Calculates the online time and writes to database
        :param event:
        :return:
        """

        [active_client_data, online_time_data] = self._client_data_from_event(event)

        # check if user already exists
        if online_time_data:
            # calculate the current online time
            online_time_new = online_time_data['online_time'] + (active_client_data['join_time'] - int(time()))
        else:
            # create client when not already in table
            pass



    def _client_data_from_event(self, event):
        """
        Fetches the needed client data from active_clients and online_time tables from the given event.
        :param event:
        :return:
        """

        # get client information from table
        active_client_data_query = "SELECT * FROM 'active_clients' WHERE 'clid' = {clid}".format(**event[0])
        active_client_data = exec_query(active_client_data_query)

        # Delete client entry
        exec_query("DELETE FROM active_clients WHERE clid = {clid}".format(**event[0]))

        # long term client data
        client_data_query = "SELECT * FROM 'online_time' " \
                            "WHERE 'client_unique_identifier' = {client_unique_identifier}".format(**active_client_data)
        online_time_data = exec_query(client_data_query)

        return active_client_data, online_time_data


    def clear_temp_data(self):
        """
        Clears temporary data including the active_clients table
        :return: None
        """

        # Clears table of active_clients
        exec_query("TRUNCATE active_clients")

    def run(self, _sentinel: object):
        """
        Main run method which will be executed in the thread.
        :param _sentinel: object which will be queued when program got stopped
        :return: None
        """

        while True:

            # wait for new item in queue
            event = self.event_queue.get()

            # check if thread must be stopped
            if event is _sentinel:
                # clear all temp data
                self.clear_temp_data()
                exit()

            # check if client joined or left the server
            reasonid = int(event[0]["reasonid"])

            # id 0: user joined the server
            if reasonid == 0:
                # add current time to be able to process
                self.join_event(event)

            # id 3: timeout, 5: kick, 6: ban, 8: left, 11: server shutdown
            elif reasonid in [3, 5, 6, 8, 11]:
                self.leave_event(event)


