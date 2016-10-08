#!/usr/bin/env python
import os
import pickle
import socket

import sys

from settings import *
FULL_PATH_SERVER_ADDRESS = os.path.join(os.path.dirname(__file__), SERVER_ADDRESS)

command = 'test'
if sys.argv[1:]:
    command = sys.argv[1]

conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
conn.connect(FULL_PATH_SERVER_ADDRESS)
test_command = {
    'command': command
}
conn.sendall(pickle.dumps(test_command))
conn.close()

print("Feeder Client: -> {} <- command sent to {}".format(command, FULL_PATH_SERVER_ADDRESS))
