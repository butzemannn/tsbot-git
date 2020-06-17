#!/usr/python

from tsbot.data.configio import read_config

class database():

    def __init__(self):
        database_credentials = read_config()["mysql"]