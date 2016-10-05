import os
import pickle
import socket
import sys
from contextlib import contextmanager

from reddit_reader import RedditReader
from settings import *

g_keep_going = True


# This should be a detached daemon as the name implies - but thanks to docker there really is no need


@contextmanager
def setup():
    # some startup cleanup - just to make sure
    try:
        os.unlink(SERVER_ADDRESS)
    except FileNotFoundError:
        pass
    # else - let other exceptions interrupt execution

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(SERVER_ADDRESS)
    sock.listen(5)
    # we want to let exceptions so far propagate up
    # This is what happens in the with block - let those excetions lead back to this so we may finalize
    try:
        yield sock
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        os.unlink(SERVER_ADDRESS)


def stop_server():
    global g_keep_going
    g_keep_going = False


def handle_request(request):
    command = request.get('command', None)
    print('Received', command)
    if command == 'stop':
        stop_server()
    elif command == 'read':
        # TODO we should catch exceptions for this part, we are a 'daemon' after all:)
        with RedditReader() as rr:
            for subreddit in request.get('subreddits', []):
                rr.consume_subreddit(subreddit)
    else:
        print('Unknown command', command, file=sys.stderr)
    print('Completed', command)


# read and execute loop
with setup() as incoming:
    while g_keep_going:
        conn, client_addr = incoming.accept()
        request = []
        while True:
            data = conn.recv(8)
            if data:
                request.append(data)
            else:
                break
        request = b''.join(request)
        request = pickle.loads(request)

        handle_request(request)

        conn.close()
