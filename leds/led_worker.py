import serial
from time import sleep
from wireless.constants import *
from wireless import Lamp, LedRing, BlinkBee, TransmitError, Timeout
import logging
from queue import LedCommandQueue



if __name__ == "__main__":
    led_queue = LedCommandQueue()

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
                elif command['action'] == 'set_ring':
                    lamp.set_static(command['data'])
                elif command['action'] == 'set_big':
                    colors = []
                    for id in range(16):
                        if id in command['data']:
                            colors.append(command['data'][id])
                        else:
                            colors.append("000000")
                    led_ring.set_colors(colors)
                    logging.debug(colors)
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
