# Copyright (c) 2021 Jan Tünnermann. All rights reserved.
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import subprocess
from flask import Flask

app = Flask(__name__)


# Configuration:
APP_HOST = '127.0.0.1' # Default is localhost
APP_PORT = 8000 

PARALLEL = True # Whether to open a parallel connection
LPT_INTERFACE = 0xD050 # Address of the parallel port interface

TCP = False # Whether to open a TCP connection
TCP_HOST = '127.0.0.1'
TCP_PORT = 50000


@app.route('/trigger/parallel/<trigger_value>')
def parallel_trigger(trigger_value):
	trigger_value = int(trigger_value)

	if(PARALLEL == False):
		status = '[Fail]'
	else:
		try:
			io.Out32(LPT_INTERFACE, trigger_value) 
			status = '[Success]'
		except:
			status = '[Fail]'

	msg = status + ' '  + 'Trigger ' + str(trigger_value)
	return(msg)

@app.route('/trigger/tcp/<trigger_value>')
def tcp_trigger(trigger_value):
	trigger_value = int(trigger_value)

	if(TCP):
		try:
			tcp_socket.send(trigger_value.to_bytes(1, 'little'))
			status = '[Success]'
		except:
			status = '[Fail]'
	
	msg = status + ' ' + 'Trigger ' + str(trigger_value)
	return(msg)

if __name__ == '__main__':

	if(PARALLEL):
		try:
			from ctypes import windll
			io = windll.LoadLibrary('inpoutx64')
			io.Out32(LPT_INTERFACE, 0) # Set to zero
		except:
			print("[Fail] Could not load Windows parallel port interface.")

	if(TCP):
		try:
			import socket
			tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			tcp_socket.connect((TCP_HOST, TCP_PORT))
		except:
			print("[Fail] Cannot connect to TCP port")	 

	app.run(host=APP_HOST, port=APP_PORT)
