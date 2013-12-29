import serial
from time import sleep
from wireless.constants import *
from wireless import Lamp, LedRing, BlinkBee, TransmitError, Timeout
import logging
import sys
sys.path.append("..")
from queue import make_led_queue

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    led_queue = make_led_queue()

    xbee_serial = serial.Serial('/dev/ttyUSB0', 9600)
    try:
        blink_bee = BlinkBee(xbee_serial)
        led_ring = LedRing(blink_bee, b'\xff\xfe', XADDR_LED_RING)
        lamp = Lamp(blink_bee, b'\xff\xfe', XADDR_LAMP)
        led_ring.set_position(0)
        led_ring.rotate_off()
        led_ring.level_green(0)

        while True:
            try:
                command = led_queue.popleft()
                if command is None:
                    logging.debug("timed out waiting for queues")
                elif command['action'] == 'set_big':
                    logging.debug(command['data'])
                    lamp.set_static(command['data'][0],command['data'][1],command['data'][2])
                elif command['action'] == 'set_ring':
                    colors = []
                    logging.debug(command['data'])
                    for id in range(16):
                        if str(id) in command['data']:
                            colors.append(command['data'][str(id)])
                        else:
                            colors.append("000000")
                    logging.debug("sending colors")
                    logging.debug(colors)
                    led_ring.set_colors(colors)
            except TransmitError, e:
                logging.exception("transmit error...")
            except Timeout, e:
                logging.exception("timeout reached...")

    except TransmitError, e:
        logging.exception("transmit error...")
    except Timeout, e:
        logging.exception("timeout reached...")
    finally:
        xbee_serial.close()
