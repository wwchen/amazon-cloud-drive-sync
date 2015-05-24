#!/usr/bin/env python

# https://localhost/#access_token=Atza%7CIQEBLjAsAhQ0UZ19f-kkkyfvkIy-gousO3FQCQIUSOUZHHlpCQBPIjDwHwuZmeiCubjPowF6FEIlyL6dGtu6smqpbt18u2SpkkDfFtRMfYZ4MVWQM35JarFuICRvXe0JaRdiC_jToK0b6SI-CPrwr9JqNYPoOd8XS-UG1Usk9tt_fLlgYNUTvSRa19WVK6OXBWteZXJ4tOF_cZkdO3BDvwsveowOwEnIA6e-y4TY0QmrHJtQdVB7zS-TnGNABN_IdZ-bsbn64fdvhcPbjpVrGtHWfyFiEvR7NLCs6aPS7wUgqxZHZ-fE7UWB91xtYkIHLI-Q-WF-0C28v71jUr8Goax9I-17DjdaDjT_1iLlA8gWnDkFaeWhIDgagBPXlXknvGW0DaQ7USBnRqrD77xr3xoNn2XY2YTjuOKjwM6VIzlwL0E&token_type=bearer&expires_in=3600&scope=clouddrive%3Aread+clouddrive%3Awrite
from bottle import get, post, route, run, template, request
from urllib import urlencode
import urllib2
import ConfigParser

CONFIG_FILE = "amazon.conf"

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

HOST = config.get('httpd', 'host')
PORT = config.get('httpd', 'port')
REDIRECT_URL = "http://{}:{}/signin".format(HOST, PORT)

CLIENT_ID = config.get('amazon', 'client_id')
CLIENT_SECRET = config.get('amazon', 'client_secret')
CODE = None


@route('/signin')
def signin_auth():
    CODE = request.params.get('code')
    scope = request.params.get('scope')

    debug = get_login_url() + '\n'
    debug += 'scope: {}\n'.format(scope)
    debug += 'code: {}\n'.format(CODE)
    access_token_request(CODE)
    print debug


@route('/signin', method='POST')
def access_token_response():
    token_type = request.params.get('token_type')
    expires_in = request.params.get('expires_in')
    refresh_token = request.params.get('refresh_token')
    access_token = request.params.get('access_token')

    print 'refresh_token', refresh_token
    return refresh_token


def access_token_request(code):
    print "Making request"
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URL
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://api.amazon.com/auth/o2/token'
    try:
        request = urllib2.Request(url, urlencode(params), headers)
        print request.get_full_url(), request.get_data(), request.header_items()
        response = urllib2.urlopen(request)
        print response.read()
    except urllib2.HTTPError as e:
        print e.code, e.reason, e.read()


def get_login_url():
    params = {
        'client_id': CLIENT_ID,
        'scope': 'clouddrive:read clouddrive:write',
        'response_type': 'code',
        'redirect_uri': REDIRECT_URL
    }
    url = 'https://www.amazon.com/ap/oa/?'
    return url + urlencode(params)


def get_code():
    return CODE


def get_config():
    print config.items('httpd')
    print config.items('amazon')


def start():
    return;


if __name__ == '__main__':
    get_config()
    print "Visit " + get_login_url()
    run(host=HOST, port=PORT, debug=True, reloader=True)
