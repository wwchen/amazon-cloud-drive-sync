#!/usr/bin/env python

import ConfigParser

# Amazon Cloud Drive api
class AmazonCloudDriveApi:
    ENDPOINT_URL = 'https://drive.amazonaws.com'

    def __init__(self, config_dict):
        """
        :param config_dict: contains the following:
          - client_id
          - client_secret
        :return:
        """
        self.config = config_dict
        start_server = self.config.read(self.CONFIG_KEY, 'start_server')
        if start_server:
            self.init_server()

    def init_server(self):
        self.client_id = config.read(self.CONFIG_KEY, 'client_id')
        self.client_secret = config.read(self.CONFIG_KEY, 'client_secret')
        self.
