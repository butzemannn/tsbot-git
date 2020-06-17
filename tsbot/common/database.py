#!/usr/python

import pymysql
import logging

# local imports
from tsbot.data.configio import read_config

# get logger from parent
logger = logging.getLogger(__name__)

# read database login credentials from config file
mysql_credentials = read_config()["mysql"]


def exec_command(command):
    """
    executes the given command on the mysql database which is given in the config file and returns
    the result of this execution
    :param command: command which will be executed in the database
    :return: returns the response of the given database
    """

    try:
        logger.info("Connecting to database and executing query...")

        # establishing connection with the given credentials
        connection = pymysql.connect(host=mysql_credentials["host"],
                                     user=mysql_credentials["user"],
                                     password=mysql_credentials["password"],
                                     db=mysql_credentials["db"])

    except Exception as e:
        logger.exception("A connection to the mysql database could not be established")
        connection.close()

    try:
        with connection.cursor() as cursor:
            logger.debug("Executed the sql query: [%]".format(command))

            # execute the given command and fetch result
            cursor.execute(command)
            result = cursor.fetchone()
            return result

    except Exception as e:
        logger.exception("There was an error while executing the sql query")

    finally:
        # close the connection
        connection.close()
        logger.debug("The sql connection was closed")