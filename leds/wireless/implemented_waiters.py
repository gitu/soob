from binascii import hexlify
from redbox.wireless import TransmitError
from redbox.wireless.Waiter import Waiter


class WaitForResponse(Waiter):
    def __init__(self, observable, timeout, frame_id):
        Waiter.__init__(self, observable, timeout)
        self.frame_id = frame_id
        self.response = None

    def receive_frame(self, frame):
        if "frame_id" in frame and frame["frame_id"] == chr(self.frame_id):
            self.done.set()
            print "found response"
            if frame["deliver_status"] == b'\x00':
                self.result = "OK"
            else:
                self.result = "ERR"
                self.exception = TransmitError(
                    "Received Deliver Status: " + hexlify(frame["deliver_status"]) + " for frame " + str(
                        self.frame_id))
            self.response = frame
            self.detach()


class WaitForConfirm(Waiter):
    def __init__(self, observable, timeout, expected_data):
        Waiter.__init__(self, observable, timeout)
        self.expected_data = expected_data
        self.confirm = None

    def receive_frame(self, frame):
        if "rf_data" in frame and frame["rf_data"] == self.expected_data:
            self.done.set()
            print "found confirm"
            self.result = "OK"
            self.confirm = frame
            self.detach()