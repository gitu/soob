import serial
from wireless.constants import *
from wireless import Lamp, LedRing, BlinkBee, TransmitError, Timeout


if __name__ == "__main__":
    xbee_serial = serial.Serial('/dev/ttyUSB0', 9600)
    try:
        blink_bee = BlinkBee(xbee_serial)
        led_ring = LedRing(blink_bee, b'\xff\xfe', XADDR_LED_RING)
        lamp = Lamp(blink_bee, b'\xff\xfe', XADDR_LAMP)

        lamp.set_color('FF00FF')
        led_ring.level_green(10)
    finally:
        xbee_serial.close()
