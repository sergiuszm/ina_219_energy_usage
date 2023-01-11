import RPi.GPIO as GPIO
from rpizero.common import Logger
from time import sleep

STATUS_UP = 'up'
STATUS_DOWN = 'down'

PIN = 16


def get_status():
    with open('/sys/class/net/wlan0/operstate', 'r') as f:
        stat = f.read()
        stat = stat.strip('\n')
        return stat


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    logger = Logger()

    prev_status = get_status()
    logger.log('WiFi >> {}'.format(prev_status))

    while True:
        try:
            status = get_status()
            if status == STATUS_UP:
                GPIO.output(PIN, 1)
            else:
                GPIO.output(PIN, 0)

            if prev_status != status:
                logger.log('WiFi >> {}'.format(status))
                prev_status = status

            sleep(3)

        except KeyboardInterrupt:
            GPIO.cleanup()
