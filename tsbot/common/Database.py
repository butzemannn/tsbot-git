#!/usr/bin/env python3

import pymysql
from logging import getLogger

# local imports
from tsbot.common.ConfigIo import ConfigIo as cio

# get logger from parent
logger = getLogger("tsbot.sql")


class Database(object):

    @staticmethod
    def exec_query(query):
        """
        Executes the given command on the mysql table which is given in the config file and returns
        the result of this execution.

        :param query:
            command which will be executed in the table

        :return: returns the response of the given table
        """

        try:
            logger.info("Connecting to table and executing query...")
            logger.debug("Establishing database connection...")

            # read table login credentials from config file
            mysql_credentials = cio.read_config()["mysql"]

            # establishing connection with the given credentials
            connection = pymysql.connect(**mysql_credentials)

            logger.debug("Database connection established")

        except ConnectionError:
            logger.exception("Failed to connect to the database")
            return

        except Exception as e:
            logger.exception("A connection to the mysql table could not be established for an unknown reason")
            return

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                logger.debug("Executed the sql query: [{}]".format(query))

                # execute the given command and fetch result
                cursor.execute(query)
                result = cursor.fetchone()
                connection.commit()

                logger.debug("Execution successful: " + str(result))
                return result

        except Exception as e:
            logger.exception("There was an error while executing the sql query")

        finally:
            # close the connection
            connection.close()
            logger.debug("The sql connection was closed")
