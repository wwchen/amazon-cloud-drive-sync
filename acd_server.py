#!/usr/bin/env python
import ConfigParser
from urllib import urlencode
import requests
import cherrypy
import json

DEBUG = False
CONFIG_KEY = "httpd"
AUTHORIZE_TRY_COUNTS = 3

# http://www.amazon.com/ap/oa?client_id=amzn1.application-oa2-client.5dab1a3e36b94fa18fd27c329f6d9591&scope=clouddrive%3Aread%20clouddrive%3Awrite&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fsignin&response_type=code

class AmazonCloudDriveServer:
    """
    This class will create a local webserver, which is required to get the authorization token callback from Amazon
    """

    def __init__(self, config_file):
        # get the info
        self._init_config(config_file)
        pass

    def log(self, message):
        if message is not None:
            cherrypy.log("AMAZON " + message)

    def start(self):
        # starts the server
        self.log("Webserver started.")
        self.log('Login at ' + self._get_login_url())
        cherrypy.quickstart(self)

    def stop(self):
        # stops the server
        pass

    def get_authorization_token(self):
        if self._access_token is None:
            return None
        return 'Bearer {}'.format(self._access_token)

    ####

    def _init_config(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self._host = config.get(CONFIG_KEY, 'host')
        self._port = config.get(CONFIG_KEY, 'port')
        self._redirect_url = "http://{}:{}/signin".format(self._host, self._port)

        self._client_id = config.get(CONFIG_KEY, 'client_id')
        self._client_secret = config.get(CONFIG_KEY, 'client_secret')

        if DEBUG:
            self.log(config.items(CONFIG_KEY))

    @cherrypy.expose
    def signin(self, code, scope):
        self.log('scope: {}'.format(scope))
        self.log('code: {}'.format(code))
        count = 0
        while count < AUTHORIZE_TRY_COUNTS:
            try:
                self._auth(code)
                self.log(str(self._get_endpoints()))
                break
            except requests.HTTPError as e:
                self.log('ERROR: Something went wrong while requesting access/refresh token')
                self.log('Request url: {}'.format(e.request.url))
                self.log('Request header: {}'.format(e.request.headers))
                self.log('{} {}: {}'.format(e.response.status_code, e.response.reason, e.response.text))
                self.log('====================')
                count += 1

    def _auth(self, code):
        response = self._request_access_token(code)
        response.raise_for_status()
        data = json.loads(response.text)
        self._token_type = data['token_type']
        self._expires_in = data['expires_in']
        self._refresh_token = data['refresh_token']
        self._access_token = data['access_token']
        self.log('refresh token: {}'.format(self._refresh_token))
        self.log('expires in: {}'.format(self._expires_in))
        self.log('access token: {}'.format(self._access_token))

    def _get_endpoints(self):
        headers = {
            'Authorization': self.get_authorization_token()
        }
        url = 'https://drive.amazonaws.com/drive/v1/account/endpoint'
        response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()
        data = json.loads(response.text)
        self._content_url = data['contentUrl']
        self._metadata_url = data['metadataUrl']
        return data

    def _request_access_token(self, code):
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'redirect_uri': self._redirect_url
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = 'https://api.amazon.com/auth/o2/token'
        response = requests.post(url, data=params, headers=headers, verify=True)
        return response

    def _refresh_access_token(self, refresh_token):
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = 'https://api.amazon.com/auth/o2/token'
        response = requests.post(url, data=params, headers=headers, verify=True)
        return response

    def _get_login_url(self):
        params = {
            'client_id': self._client_id,
            'scope': 'clouddrive:read clouddrive:write',
            'response_type': 'code',
            'redirect_uri': self._redirect_url
        }
        url = 'https://www.amazon.com/ap/oa/?'
        return url + urlencode(params)


