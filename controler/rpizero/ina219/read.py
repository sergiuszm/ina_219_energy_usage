import RPi.GPIO as GPIO
from ina219 import INA219
from ina219 import DeviceRangeError
from rpizero.common import Logger, get_timestamp
from time import sleep
import datetime
import os
import socket

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.6
logger = None
ina = None

PIN_EXP = 25
PIN_LED = 19
EXP_NR = 0
GPIO.setmode(GPIO.BCM)
PATH = "/home/pi/data/power/"


def read():
    try:
        timestamp = get_timestamp()
        current = ina.current()
        voltage = ina.voltage()
        power1 = ina.power()
        power2 = current * voltage

        return "%d | %.3f | %.3f | %.3f | %.3f" % (timestamp, current, voltage, power1, power2)
    except DeviceRangeError as e:
        logger.log("Current overflow")


def save_to_file(data):
    global EXP_NR

    def _get_date():
        time_object = datetime.datetime.now()
        date = time_object.strftime("%Y-%m-%d")
        return date

    hostname = socket.gethostname()

    if not os.path.exists(PATH):
        os.makedirs(PATH)
    filename = "{}ina219_{}-{}-{}".format(PATH, hostname, _get_date(), EXP_NR)
    with open(filename, 'a') as out:
        for x in data:
            out.write(str(x) + '\n')


def get_exp_nr():
    files = os.listdir(PATH)

    return len(files)


if __name__ == "__main__":
    global EXP_NR

    try:
        logger = Logger()
        EXP_NR = get_exp_nr()
        GPIO.setup(PIN_EXP, GPIO.IN)
        GPIO.setup(PIN_LED, GPIO.OUT, initial=GPIO.LOW)

        ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
        ina.configure(ina.RANGE_16V, ina.GAIN_2_80MV)
        logger.log('INA219 configured!')
        logger.log('Next experiment: #{}'.format(EXP_NR))

        if ina is not None:
            readings = []
            prev_pin_val = GPIO.input(PIN_EXP)

            while True:
                pin_val = GPIO.input(PIN_EXP)

                if prev_pin_val != pin_val:

                    if pin_val > 0:
                        EXP_NR = get_exp_nr()
                        logger.log('#{}: Exp started!'.format(EXP_NR))
                        GPIO.output(PIN_LED, 1)
                        readings = []
                    else:
                        logger.log('#{}: Exp ended!'.format(EXP_NR))
                        logger.log('#{} Saving!'.format(EXP_NR))
                        save_to_file(readings)
                        logger.log('#{} Saved!'.format(EXP_NR))
                        GPIO.output(PIN_LED, 0)

                if pin_val:
                    readings.append(read())
                    sleep(0.2)

                prev_pin_val = pin_val

    except KeyboardInterrupt:
        logger.log('Interrupted!')
        GPIO.cleanup()
