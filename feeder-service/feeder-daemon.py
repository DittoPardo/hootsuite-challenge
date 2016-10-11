import os
import pickle
import socket
import sys
from contextlib import contextmanager

from jobcontrol import job_control
from reddit_reader import RedditReader
from settings import *

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
        sock.close()
        os.unlink(SERVER_ADDRESS)


def handle_request(request):
    command = request.get('command', None)
    print('Received', command)
    if command == 'stop':
        job_control.stop_server()
    elif command == 'read':
        # TODO we should catch exceptions for this part, we are a 'daemon' after all:)
        with RedditReader() as rr:
            for subreddit in request.get('subreddits', []):
                rr.consume_subreddit(subreddit)
                if job_control.should_exit:
                    return
    elif command == 'test':
        print("Received test command.")
    else:
        print('Unknown command', command, file=sys.stderr)
    print('Completed', command)


# read and execute loop
with setup() as incoming:
    while job_control.keep_going:
        try:
            # Can't seem to get this syscall interrupted by signals no matter the state of siginterrupt
            # raising exception works, but then again it will hurt any other part of code
            # This is why JobControl raises exception as the last resort
            conn, client_addr = incoming.accept()
        except InterruptedError:
            if job_control.should_exit:
                break

        request = []
        while job_control.keep_going:
            data = conn.recv(4096)
            if data:
                request.append(data)
            else:
                break

        if request:
            request = b''.join(request)
            request = pickle.loads(request)
            handle_request(request)

        conn.close()
