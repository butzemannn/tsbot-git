#!/usr/python

import json

class configio():

    config_path = "tsbot.cfg"

    def __init__(self):
        pass

    def read_config(self):
        with open(self.config_path) as json_data_file:
            data = json.load(json_data_file)
            return data

    def write_config(self, data):
        with open(self.config_path) as json_data_file:
            json.dump(data, json_data_file)
