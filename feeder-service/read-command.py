#!/usr/bin/env python
import os
import pickle
import socket
import time


from settings import *
FULL_PATH_SERVER_ADDRESS = os.path.join(os.path.dirname(__file__), SERVER_ADDRESS)

conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# This is a hack to make sure the deamon is up.
# crontab is installed before the deamon is started
# crontab executes this command at boot.
# TODO find a better way than making all read-commands 1 second slower...
time.sleep(1)
conn.connect(FULL_PATH_SERVER_ADDRESS)
stop_command = {
    'command': 'read',
    'subreddits': SUBREDDITS,
}
conn.sendall(pickle.dumps(stop_command))
conn.close()

print("Feeder Client: -> read <- command sent to {}".format(FULL_PATH_SERVER_ADDRESS))
