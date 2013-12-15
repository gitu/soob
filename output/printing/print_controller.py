import io
import re
import threading
import traceback
import urllib
from PIL import Image
import requests
from time import sleep
import sys


def inverse_on(printer, cmd):
    printer.inverseOn()


def inverse_off(printer, cmd):
    printer.inverseOff()


def underline_on(printer, cmd):
    printer.underlineOn()


def underline_off(printer, cmd):
    printer.underlineOff()


def bold_on(printer, cmd):
    printer.boldOn()


def bold_off(printer, cmd):
    printer.boldOff()


def size(printer, cmd):
    try:
        printer.setSize(cmd[4:])
    except:
        printer.write("could not set size: " + cmd)


def print_image(printer, cmd):
    try:
        fd = urllib.urlopen(cmd[11:-1])
        image_file = io.BytesIO(fd.read())
        printer.printImage(Image.open(image_file), True)
    except:
        printer.write("could not print image: " + cmd)
        print "error parsing image: " + cmd + " - " + str(sys.exc_info()[0])
        traceback.print_exc()


COMMANDS = {
    'inverseON': inverse_on,
    'inverseOFF': inverse_off,
    'underlineON': underline_on,
    'underlineOFF': underline_off,
    'boldON': bold_on,
    'boldOFF': bold_off,
    'size.': size,
    'printIMAGE<[^>]*>': print_image
}

SPLIT_REGEX = re.compile("(##" + "##|##".join(COMMANDS) + "##)")
COMMAND_REGEX = re.compile("##(" + "|".join(COMMANDS) + ")##")


class PrintController(threading.Thread):
    current_command = ""

    def __init__(self, controller, printer):
        super(PrintController, self).__init__()
        self.url = controller.config.get("RedFlag", "BaseURL")
        if controller.config.has_option("RedFlag", "Proxy"):
            self.proxy = controller.config.get("RedFlag", "Proxy")
            self.proxies = {"http": self.proxy}
        else:
            self.proxies = None
        self.exit_flag = 0
        self.controller = controller
        self.printer = printer
        self.lock = threading.Lock()

    def request_stop(self):
        self.exit_flag = 1

    def run(self):
        while not self.exit_flag:
            p = requests.get(self.url + "print", proxies=self.proxies)
            if p.status_code == 200:
                try:
                    self.print_formatted_text(p.text)
                except:
                    print "failed to print"
                    print "- " + str(sys.exc_info()[0])
                    print "text: "
                    print traceback.print_exc() + str(p.text)
            sleep(4)

    def print_formatted_text(self, print_text):
        try:
            self.lock.acquire()
            self.printer.wake()
            self.printer.setDefault()
            for m in SPLIT_REGEX.split(print_text):
                if SPLIT_REGEX.match(m):
                    for c in COMMANDS:
                        matcher = re.compile("##(" + c + ")##")
                        match = matcher.match(m)
                        if match:
                            COMMANDS[c](self.printer, str(match.group(1)))
                else:
                    self.printer.write(m.encode('utf-8'))
            self.printer.write('\n')
            self.printer.sleep()
        finally:
            self.lock.release()


if __name__ == '__main__':
    text = "abc##underlineON##is##underline##asdf##printIMAGE<https://wiki.jenkins-ci.org/download/attachments/2916393/headshot.png>##"
    for m in SPLIT_REGEX.split(text):
        if SPLIT_REGEX.match(m):
            print "COMMANDO: " + COMMAND_REGEX.match(m).group(1)
        else:
            print m