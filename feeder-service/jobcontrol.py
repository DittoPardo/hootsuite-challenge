import signal

from settings import INTERRUPT_GRACE_PERIOD

__all__ = [
    'job_control',
]


class JobControl(object):
    def __init__(self):
        # interacting with this won't touch alarm logic
        # use should_exit property for that
        self.keep_going = True
        signal.signal(signal.SIGINT, self.stop_server)
        signal.signal(signal.SIGTERM, self.stop_server)
        signal.signal(signal.SIGALRM, self.stop_by_exception)

    def stop_server(self, signum=None, frame=None, request=None):
        if signum is None:
            self.keep_going = False
        else:
            self.should_exit = True

    def stop_by_exception(self, signum, frame):
        raise InterruptedError(signal)

    @property
    def should_exit(self):
        if not self.keep_going:
            # reset the alarm - we are in a non-blocking part of code that is able to check should_exit
            signal.alarm(0)
            return True
        return False

    @should_exit.setter
    def should_exit(self, val):
        self.keep_going = not val
        if val:
            # some syscalls won't give up no matter the siginterrupt state. Use exception only as a last resort
            # Any part of the code should exit by checking keep_going flag, in the INTERRUPT_GRACE_PERIOD
            # else we shall exit by exception
            signal.alarm(INTERRUPT_GRACE_PERIOD)
        else:
            signal.alarm(0)


job_control = JobControl()
