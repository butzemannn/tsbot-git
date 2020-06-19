#!/usr/python

# local imports
from tsbot.io.database import exec_query


class DBQueryHandler(object):

    def __init__(self):
        pass

    @staticmethod
    def get_db_entry(table: str, identifier):
        """
        Gives the table entry for the client with the given clid from the given table

        :param table:
            The table from which the entry will be returned
        :param identifier:
            clientid or client_unique_identifier which will be used for identification of the table entry, which
            will be returned

        :return: Returns the table entry for the given clid or client_unique_identifier
        :rtype: dict
        """
        # has to use different identification keys depending on table
        if table == "active_clients":
            query = "SELECT * FROM {} WHERE clid = {};".format(table, identifier)

        elif table == "online_time":
            query = "SELECT * FROM {} WHERE client_unique_identifier = '{}';".format(table, identifier)
        else:
            raise ValueError("The specified table is unknown")

        return exec_query(query)

    @staticmethod
    def insert_db_entry(table: str, **data: dict):
        """
        Inserts the data into the given table

        Note:
            The dictionary data should include most of the following keys:
                client_nickname,
                client_unique_identifier,
                client_database_id,
                identifier,
                client_servergroups,
                join_time,

        :param table:
            Name of the table into which the data should be inserted
        :param data:
            The data which will be inserted into the table

        :return: None
        """

        if table == "active_clients":
            query = "INSERT INTO {} (client_nickname, client_unique_identifier, client_database_id, clid, client_servergroups, join_time) " \
                    "VALUES ('{client_nickname}', '{client_unique_identifier}', {client_database_id}, {clid}, '{client_servergroups}' , {join_time});".format(table, **data)
        elif table == "online_time":
            query = "INSERT INTO {} (client_nickname, client_unique_identifier, client_database_id, client_servergroups, online_time) " \
                    "VALUES ('{client_nickname}', '{client_unique_identifier}', {client_database_id}, '{client_servergroups}', {online_time})".format(table, **data)
        else:
            raise ValueError("The specified table is not known.")

        exec_query(query)

    @staticmethod
    def update_online_time_entry(**data: dict):
        """
        Updates the user with the used data

        :param table:
        :param data:
        :return:
        """
        query = "UPDATE online_time " \
                "SET client_nickname = '{client_nickname}', client_servergroups = '{client_servergroups}', online_time = {online_time} " \
                "WHERE client_unique_identifier = '{client_unique_identifier}';".format(**data)
        exec_query(query)

    @staticmethod
    def delete_entry_from_clid(table: str, clid):
        """
        Deletes the table entry for the client with the given clid from the given table

        :param table:
            The table from which the entry will be deleted
        :param clid:
            clientid of the user whose data will be deleted

        :return: None
        """
        exec_query("DELETE FROM {} WHERE clid = {};".format(table, clid))

    @staticmethod
    def clear_table(table: str):
        """
        Clears the given table

        :param table:
            Table which should be cleard

        :return: None
        """
        exec_query("TRUNCATE {}".format(table))
