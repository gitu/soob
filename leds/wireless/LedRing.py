from binascii import unhexlify, hexlify
from string import join
from struct import pack
from .WLControl import WLControl


class LedRing(WLControl):
    commands = {
        "full": {"cmd_byte": b'\x00', "pack": "48B"},
        "color": {"cmd_byte": b'\x01', "pack": "BBB"},
        "set_position": {"cmd_byte": b'\x02', "pack": "B"},
        "jump": {"cmd_byte": b'\x03', "pack": "B"},
        "level": {"cmd_byte": b'\x04', "pack": "BBBB"},
        "level_red": {"cmd_byte": b'\x05', "pack": "B"},
        "level_green": {"cmd_byte": b'\x06', "pack": "B"},
        "level_blue": {"cmd_byte": b'\x07', "pack": "B"},
        "red": {"cmd_byte": b'\x08'},
        "green": {"cmd_byte": b'\x09'},
        "blue": {"cmd_byte": b'\x0a'},
        "rotate_left": {"cmd_byte": b'\x0b'},
        "rotate_right": {"cmd_byte": b'\x0c'},
        "rotate_off": {"cmd_byte": b'\x0d'},
        "set_fade": {"cmd_byte": b'\x0e', "pack": ">16H"},
        "fade_off": {"cmd_byte": b'\x0f'},
        "set_brightness": {"cmd_byte": b'\x10', "pack": "B"},
        "use_gamma": {"cmd_byte": b'\x11'},
        "gamma_off": {"cmd_byte": b'\x12'},
    }

    def __init__(self, blink_bee, addr, addr_long):
        WLControl.__init__(self, blink_bee, addr, addr_long)

    def set_level_color(self, color, level):
        self.level(unhexlify(hexlify(chr(level)) + color))

    def set_colors(self, colors):
        if len(colors) == 16:
            self.tx("full",unhexlify(join(colors, "")))
        else:
            print "length should be 16"

    def set_fade(self, fades):
        if len(fades) == 16:
            self.tx("set_fade", pack('>16H', *fades))
        else:
            print "length should be 16"