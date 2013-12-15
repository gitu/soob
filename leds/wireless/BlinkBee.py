import itertools
from .FrameConsumer import FrameConsumer
from .implemented_waiters import WaitForResponse, WaitForConfirm
from .xbee import ZigBee


class BlinkBee():
    REQUEST = b'\x01'
    RECEIVED_COMMAND = b'\x02'

    def __init__(self, serial):
        self.frame_consumer = FrameConsumer()
        self.xbee = ZigBee(serial, callback=self.frame_consumer.receive_frame, escaped=True)
        self.frame_cycle = itertools.cycle(range(1, 255))

    def send(self, addr_long, addr_short, expected_confirm_command, data, timeout):
        frame_id = self.frame_cycle.next()

        wait_response = WaitForResponse(self.frame_consumer, timeout, frame_id)
        wait_confirm = WaitForConfirm(self.frame_consumer, timeout,
                                      BlinkBee.RECEIVED_COMMAND + expected_confirm_command)

        wait_confirm.start()
        wait_response.start()

        self.xbee.tx(
            frame_id=chr(frame_id),
            dest_addr_long=addr_long,
            dest_addr=addr_short,
            data=data
        )

        wait_response.join(timeout)
        print "response " + str(wait_response.result)
        if wait_response.exception:
            raise wait_response.exception

        wait_confirm.join(timeout)
        print "confirm  " + str(wait_confirm.result)
        if wait_confirm.exception:
            raise wait_confirm.exception