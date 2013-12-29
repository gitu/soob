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


class PrintController():
    current_command = ""

    def __init__(self, printer):
        self.printer = printer
        self.lock = threading.Lock()

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