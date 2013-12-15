from celery import Celery
import serial
from wireless import Lamp, LedRing, BlinkBee, TransmitError, Timeout
app = Celery()

CONTROLLER =  b'\x00\x13\xa2\x00\x40\xb0\xa1\xad'
LED_RING = b'\x00\x13\xa2\x00\x40\xab\x97\x64'
BLINK = b'\x00\x13\xa2\x00\x40\xac\xc4\x90'


from celery.task import Task
from celery.registry import tasks
from celery.signals import task_prerun

_precalc_table = {}

class PowersOfTwo(Task):

    def run(self, x):
        if x in _precalc_table:
            return _precalc_table[x]
        else:
            return x ** 2
tasks.register(PowersOfTwo)


def _precalc_numbers(**kwargs):
    if not _precalc_table: # it's empty, so haven't been generated yet
        for i in range(1024):
            _precalc_table[i] = i ** 2


# need to use registered instance for sender argument.
task_prerun.connect(_precalc_numbers, sender=tasks[PowerOfTwo.name])


@app.task
def blink_

if __name__ == '__main__':
    app.worker_main()

