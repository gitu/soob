import threading
from time import sleep
import traceback
import sys


class BlinkWorker(threading.Thread):
    def __init__(self, blink):
        super(BlinkWorker, self).__init__()
        self.exit_flag = 0
        self.lock = threading.Lock()
        self.blink = blink
        self.c_r = "OFF"
        self.c_g = "OFF"
        self.c_b = "OFF"
        self.blink_r, self.state_r = parse_text(self.c_r)
        self.blink_g, self.state_g = parse_text(self.c_g)
        self.blink_b, self.state_b = parse_text(self.c_b)
        self.parse()


    def request_stop(self):
        print "blink worker stop requested"
        self.exit_flag = 1

    def update(self, r, g, b):
        self.c_r = r
        self.c_g = g
        self.c_b = b
        self.parse()

    def parse(self):
        self.lock.acquire()
        try:
            self.blink_r, self.state_r = parse_text(self.c_r)
            self.blink_g, self.state_g = parse_text(self.c_g)
            self.blink_b, self.state_b = parse_text(self.c_b)
        except:
            print "error parsing command:", sys.exc_info()[0]
            traceback.print_exc()
        finally:
            self.lock.release()

    def worker(self):
        i = 0
        last_color = "000000"
        current_color = last_color
        while not self.exit_flag:
            i += 1
            self.lock.acquire()
            try:
                current_color = ('FF' if self.state_r else '00') + \
                                ('FF' if self.state_g else '00') + \
                                ('FF' if self.state_b else '00')
            finally:
                self.lock.release()
            if current_color != last_color:
                self.blink.set_color(current_color)
                last_color = current_color
            sleep(0.1)

    def run(self):
        self.worker()
        self.blink.set_color("000000")


def parse_text(text):
    if text == 'OFF':
        return 0, False
    elif text == 'ON':
        return 0, True
    else:
        return int(text.split(" ")[1]), True
