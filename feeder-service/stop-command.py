#!/usr/bin/env python
import os
import pickle
import socket

from settings import *
FULL_PATH_SERVER_ADDRESS = os.path.join(os.path.dirname(__file__), SERVER_ADDRESS)


conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
conn.connect(FULL_PATH_SERVER_ADDRESS)
stop_command = {
    'command': 'stop'
}
conn.sendall(pickle.dumps(stop_command))
conn.close()

print("Feeder Client: -> stop <- command sent to {}".format(FULL_PATH_SERVER_ADDRESS))
