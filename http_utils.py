#!/usr/bin/env python
import abc
from urllib2 import urlopen, Request, HTTPError


class BaseHttpRequest:
    params = {}
    headers = {}

    def __init__(self, default_params = None, default_headers = None):
        self.params = default_headers if not None
        self.headers = default_headers if not None

    def get_request(self, url, params, headers = None):
        """
        Make a GET request
        :param url:
        :param params:
        :return:
        """

    def post_request(self, url, params, headers = None):
        """
        Make a POST request
        :param url:
        :param params:
        :param headers:
        :return:
        """
        try:
            r = urlopen(Request(self.ENDPOINT_URL, params, headers))
            return HTTPResponse(r.code, r.reseason, r.read())
        except HTTPError as e:
            return HTTPResponse(e.code, e.reason, e.read())

class AmazonCloudDriveHttpRequest (BaseHttpRequest):
    _access_token = None
    _params = None

    def __init__(self, access_token = None):
        self.access_token = access_token
        BaseHttpRequest.__init__(self, self._params)

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token
        self._params = {
            'Authorization': 'Bearer %s' % (access_token)
        }

##########

class HTTPResponse:
    code = None
    reason = None
    content = None

    def __init__(self, code, reason, content):
        self.code = code
        self.reason = reason
        self.content = json.parse(content) # todo

    def get_conent(self):
        return self.content



