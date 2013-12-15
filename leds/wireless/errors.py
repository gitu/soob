
class Timeout(Exception):
    def __init__(self, msg):
        self.msg = msg


class TransmitError(Exception):
    def __init__(self, msg):
        self.msg = msg
