#!/usr/bin/env python
from acd_server import AmazonCloudDriveServer
import time


if __name__ == '__main__':
    print "Launching server app..."  # todo it's faked right now
    server = AmazonCloudDriveServer('amazon.conf')
    server.start()
    print "Go to this url: " + server.get_login_url()
    # somehow realize that the token is gotten
    #wait_for_signin()
    #get_auth_token()
