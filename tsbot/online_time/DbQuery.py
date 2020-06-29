#!/usr/bin/env python3

from logging import getLogger

# local imports
from tsbot.common.Database import Database as db

logger = getLogger("tsbot.sql")


class DbQuery(object):

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

        logger.debug("Fetching Database entry: table=<{}>, identifier=<{}>".format(table, identifier))

        # has to use different identification keys depending on table
        if table == "active_clients":
            query = "SELECT * FROM {} WHERE clid = {};".format(table, identifier)

        elif table == "online_time":
            query = "SELECT * FROM {} WHERE client_unique_identifier = '{}';".format(table, identifier)
        else:
            logger.error("The specified table is unknown: <{}>".format(table))
            raise ValueError("The specified table is unknown")

        return db.exec_query(query)

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
        logger.debug("Inserting Database entry: table=<{}>, data=<{}>".format(table, data))

        # different query because of different stored information depending on table name
        if table == "active_clients":
            query = "INSERT INTO {} (client_nickname, client_unique_identifier, client_database_id, clid, client_servergroups, join_time, afk_time, client_description, client_country) " \
                    "VALUES ('{client_nickname}', '{client_unique_identifier}', {client_database_id}, {clid}, '{client_servergroups}' , {join_time}, 0, '{client_description}', '{client_country}');".format(table, **data)

        elif table == "online_time":
            query = "INSERT INTO {} (client_nickname, client_unique_identifier, client_database_id, client_servergroups, online_time) " \
                    "VALUES ('{client_nickname}', '{client_unique_identifier}', {client_database_id}, '{client_servergroups}', {online_time});".format(table, **data)

        elif table == "client_history":
            query = "INSERT INTO {} (client_nickname, client_description, client_unique_identifier, clid, client_database_id, client_servergroups, " \
                    "client_created, client_totalconnections, client_country, client_lastip, join_time, leave_time, online_time, afk_time) " \
                    "VALUES ('{client_nickname}', '{client_description}', '{client_unique_identifier}', {clid}, {client_database_id}, '{client_servergroups}', " \
                    "{client_created}, {client_totalconnections}, '{client_country}', '{client_lastip}', {join_time}, {leave_time}, {online_time}, {afk_time});".format(table, **data)

        else:
            logger.error("The specified table is not known: <{}>".format(table))
            raise ValueError("The specified table is not known.")

        db.exec_query(query)

    @staticmethod
    def update_online_time_entry(**data: dict):
        """
        Updates the user with the used data

        :param table:
        :param data:
        :return:
        """
        logger.debug("Updating table online_time: data=<{}>".format(data))

        query = "UPDATE online_time " \
                "SET client_nickname = '{client_nickname}', client_servergroups = '{client_servergroups}', online_time = {online_time}, client_servergroups = '{client_servergroups}'" \
                "WHERE client_unique_identifier = '{client_unique_identifier}';".format(**data)

        db.exec_query(query)

    @staticmethod
    def update_afk_time(self, **data):
        # TODO comment and logging

        logger.debug("Updating afk time")
        query = "UPDATE active_clients SET afk_time = afk_time + {client_idle_time} WHERE clid = {clid};". format(**data)
        db.exec_query(query)

    @staticmethod
    def delete_entry_from_clid(table: str, clid: int):
        """
        Deletes the table entry for the client with the given clid from the given table

        :param table:
            The table from which the entry will be deleted
        :param clid:
            clientid of the user whose data will be deleted

        :return: None
        """

        logger.debug("Deleting user from table: table={}, clid={}".format(table, clid))
        db.exec_query("DELETE FROM {} WHERE clid = {};".format(table, clid))

    @staticmethod
    def clear_table(table: str):
        """
        Clears the given table

        :param table:
            Table which should be cleard

        :return: None
        """

        logger.debug("Clearing table: table=<{}>".format(table))
        db.exec_query("TRUNCATE {};".format(table))
