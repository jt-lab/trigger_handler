# Copyright (c) 2021 Jan Tünnermann. All rights reserved.
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import subprocess
from flask import Flask

app = Flask(__name__)


# Configuration:
LPT_INTERFACE = 0xD050 # Address of the parallel port interface
HOST = '127.0.0.1' # Defaul is localhost
PORT = 8000 


@app.route('/trigger/parallel/<trigger_value>')
def parallel_trigger(trigger_value):
	trigger_value = int(trigger_value)

	try:
		io.Out32(LPT_INTERFACE, trigger_value) 
		status = '[Success]'
	except:
		status = '[Fail]'
	msg = status + ' '  + 'Trigger ' + str(trigger_value)
	return(msg)
    
if __name__ == '__main__':

	try:
		from ctypes import windll
		io = windll.LoadLibrary('inpoutx64')
		io.Out32(LPT_INTERFACE, 0) # Set to zero
	except:
		print("[Fail] Could not load Windows parallel port interface.") 

	app.run(host=HOST, port=PORT)
