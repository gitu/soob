__author__ = 'flsc'
from datetime import datetime


class BlinkMSim():
    def __init__(self):
        self.last_hex = "000000"

    def reset(self):
        pass

    def fade_to_hex(self, hex_color):
        if self.last_hex != hex_color:
            print (str(datetime.now()) + " BLINK: fade_to_hex: " + hex_color)
            self.last_hex = hex_color

    def go_to_hex(self, hex_color):
        if self.last_hex != hex_color:
            print (str(datetime.now()) + " BLINK: go_to_hex: " + hex_color)
            self.last_hex = hex_color
