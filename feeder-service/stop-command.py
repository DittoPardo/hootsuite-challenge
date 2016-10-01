#!/usr/bin/env python
import pickle
import socket


from settings import *

conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
conn.connect(SERVER_ADDRESS)
stop_command = {
    'command': 'stop'
}
conn.sendall(pickle.dumps(stop_command))
conn.close()
