from binascii import hexlify, unhexlify
import sys
import traceback


class FrameConsumer():
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    #noinspection PyBroadException
    def receive_frame(self, frame):
        print "## received frame: " + frame["id"]
        #for x in frame:
        #    print "##  " + '{0: <16}'.format(x) + ": " + hexlify(frame[x])
        if "rf_data" in frame:
            print "   received data: " + hexlify(frame["rf_data"])

        for observer in self._observers:
            try:
                observer.receive_frame(frame)
            except:
                print "swallowed exception"
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print repr(traceback.format_exception(exc_type, exc_value,
                                                      exc_traceback))