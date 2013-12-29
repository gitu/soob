import serial
from time import sleep
import logging
from queue import LedCommandQueue
from queue.PrintQueue import PrintQueue
from adafruit import Adafruit_Thermal
from print_controller import PrintController


if __name__ == "__main__":
    print_queue = PrintQueue()

    try:
        printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
        print_controller = PrintController(printer)
        while True:
            try:
                print_job = print_queue.popleft()
                if print_job is None:
                    logging.debug("timed out waiting for queues")
                else:
                    logging.debug(print_job)
                    print_controller.print_formatted_text(print_job)
            except Exception, e:
                logging.exception("timeout reached...")
    except Exception, e:
        logging.exception("timeout reached...")
