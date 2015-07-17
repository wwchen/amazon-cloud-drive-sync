#!/usr/bin/env python
from acd_api import AmazonCloudDriveApi
from acd_server import AmazonCloudDriveServer
import time


if __name__ == '__main__':
    print "Launching server app..."  # todo it's faked right now
    server = AmazonCloudDriveServer('amazon.conf')
    client = AmazonCloudDriveApi()
    server.start()
    print "Go to this url: " + server._get_login_url()
    # somehow realize that the token is gotten
    #wait_for_signin()
    while auth_token is None:
        auth_token = server.get_authorization_token()

    client.access_token = auth_token
    client.metadata_url = server._metadata_url # todo fix
    client.content_url = server._content_url
    print "*** Auth token fetched"
    client.upload_file(open('acd_server.py'), 'acd_server.py')

