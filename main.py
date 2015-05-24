#!/usr/bin/env python
import server
import time

def wait_for_signin():
	return 'ANJyNCEHbzhDzNGnLSuD'
	while (server.get_code() == None):
		time.sleep(2)
	print "Got the code: " + server.get_code()

def get_auth_token():
	return;

if __name__ == '__main__':
	print "Launching server app..." # todo it's faked right now
	#server.start()
	print "Go to this url: " + server.get_login_url()
	# somehow realize that the token is gotten
	wait_for_signin()
	get_auth_token()

