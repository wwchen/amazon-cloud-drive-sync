#!/usr/bin/env python

import ConfigParser
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError

# Amazon Cloud Drive api
class AmazonCloudDriveApi:
    ENTRYPOINT_URL = 'https://drive.amazonaws.com/drive/v1/account/endpoint'
    content_url = None
    metadata_url = None
    access_token = None

    def __init__(self, access_token):
        self.access_token = access_token
        self.init_urls()

    def init_urls(self):
        response = HTTPRequest.make_post_request(self.ENTRYPOINT_URL)
        if response.code == 200:
            self.content_url = response.content.get('contentUrl')
            self.metadata_url = response.content.get('metadataUrl')
        else:
            raise IOError("didn't fetch urls: " + response.content)



