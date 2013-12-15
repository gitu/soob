import socket
import struct
from time import sleep
import logging
import fcntl

from adafruit import Adafruit_CharLCDPlate


logging.basicConfig(level=logging.DEBUG)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


logging.info("starting")

lcd = Adafruit_CharLCDPlate()
lcd.clear()

lcd.backlight(lcd.ON)
lcd.message("Adafruit RGB LCD\nPlate w/Keypad!")
sleep(1)

# Cycle through backlight colors
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
for c in col:
    lcd.backlight(c)
    sleep(.5)

while True:
    try:
        lcd.backlight(lcd.OFF)
        logging.debug("will fetch ip address")
        ip_address = get_ip_address('wlan0')
        lcd.backlight(lcd.ON)
        logging.info("got ip address " + str(ip_address))
        lcd.clear()
        lcd.message("My IP:\n" + str(ip_address))
        logging.debug("I'm done showing the ip address")
        sleep(100)
        logging.debug("next run")
    except Exception, ex:
        logging.exception("Something awful happened!")