import threading
from redbox.wireless import Timeout


class Waiter(threading.Thread):
    def __init__(self, observable, timeout):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.result = None
        self.exception = None
        self.observable = observable
        self.observable.attach(self)
        self.done = threading.Event()

    def detach(self):
        self.observable.detach(self)

    def run(self):
        if not self.done.wait(self.timeout):
            self.result = "ERR"
            self.exception = Timeout("Thread was waiting for " + str(self.timeout))
            self.detach()