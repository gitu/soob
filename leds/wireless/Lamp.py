from redbox.wireless.WLControl import WLControl
from binascii import unhexlify


class Lamp(WLControl):
    commands = {
        "set_static": {"cmd_byte": b'\x00', "pack": "BBB"},
        "set_script": {"cmd_byte": b'\x01', "pack": "B"},
        "blink_red":  {"cmd_byte": b'\x02'},
        "gen_script": {"cmd_byte": b'\x03', "pack": "BBBBBB"},
        "fade_speed": {"cmd_byte": b'\x04', "pack": "H"},
    }

    def __init__(self, blink_bee, addr, addr_long):
        WLControl.__init__(self, blink_bee, addr, addr_long)

    def set_color(self, hex_color):
        self.set_static(unhexlify(hex_color))
