import re
import threading
from time import sleep
import traceback
import requests
import sys
from blink_worker import BlinkWorker

COMMAND = re.compile('([^ ]*) (.*)')

http_proxy = "proxy.corproot.net:8079"
https_proxy = "proxy.corproot.net:8079"
ftp_proxy = "proxy.corproot.net:8079"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}


class BlinkController(threading.Thread):
    FADE_SPEED = 20
    current_command = ""

    def __init__(self, controller, blinkm):
        super(BlinkController, self).__init__()
        self.exit_flag = 0
        self.controller = controller
        self.url = controller.config.get("RedFlag", "BaseURL")
        if controller.config.has_option("RedFlag", "Proxy"):
            self.proxy = controller.config.get("RedFlag", "Proxy")
            self.proxies = {"http": self.proxy}
        else:
            self.proxies = None
        self.c_r = "OFF"
        self.c_g = "OFF"
        self.c_b = "OFF"
        self.worker = BlinkWorker(blinkm)

    def request_stop(self):
        print "blink controller stop requested"
        self.exit_flag = 1
        self.worker.request_stop()

    def check_state(self):
        try:
            r = requests.get(self.url + "store/blink/red", proxies=self.proxies)
            g = requests.get(self.url + "store/blink/green", proxies=self.proxies)
            b = requests.get(self.url + "store/blink/blue", proxies=self.proxies)
            if r.status_code == 200:
                self.c_r = r.text
            if b.status_code == 200:
                self.c_b = b.text
            if g.status_code == 200:
                self.c_g = g.text
            self.worker.update(self.c_r, self.c_g, self.c_b)
        except:
            print "error fetching:", sys.exc_info()[0]
            traceback.print_exc()

    def run(self):
        print("will now start "+str(self))
        self.worker.start()
        while not self.exit_flag:
            self.check_state()
            sleep(2)
        self.worker.join()



