import serial
from time import sleep
from wireless.constants import *
from wireless import Lamp, LedRing, BlinkBee, TransmitError, Timeout
import logging


if __name__ == "__main__":
    xbee_serial = serial.Serial('/dev/ttyUSB0', 9600)
    try:
        blink_bee = BlinkBee(xbee_serial)
        led_ring = LedRing(blink_bee, b'\xff\xfe', XADDR_LED_RING)
        lamp = Lamp(blink_bee, b'\xff\xfe', XADDR_LAMP)
        lamp.set_static(0,255,0)
        
        led_ring.set_position(0)
        led_ring.rotate_off()
        led_ring.level_green(2)
        sleep(2)
    except TransmitError, e:
        raw_input("Press Enter to continue...")
    except Timeout, e:
        print "Reached Timeout: " + e.msg
    finally:
        xbee_serial.close()
