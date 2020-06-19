#!/usr/python

import pymysql
from logging import getLogger

# local imports
from tsbot.io.configio import read_config

# get logger from parent
logger = getLogger(__name__)

# read database login credentials from config file
mysql_credentials = read_config()["mysql"]


def exec_query(query):
    """
    Executes the given command on the mysql database which is given in the config file and returns
    the result of this execution.
    :param query: command which will be executed in the database
    :return: returns the response of the given database
    """

    try:
        logger.info("Connecting to database and executing query...")

        # establishing connection with the given credentials
        connection = pymysql.connect(**mysql_credentials)

    except Exception as e:
        logger.exception("A connection to the mysql database could not be established")
        return

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            logger.debug("Executed the sql query: [%]".format(query))

            # execute the given command and fetch result
            cursor.execute(query)
            result = cursor.fetchone()
            connection.commit()
            return result

    except Exception as e:
        logger.exception("There was an error while executing the sql query")

    finally:
        # close the connection
        connection.close()
        logger.debug("The sql connection was closed")