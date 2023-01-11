import RPi.GPIO as GPIO
import os
import time
from rpizero.common import Logger

PIN = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
logger = Logger()

while True:
    if GPIO.input(PIN):
        logger.log("Shutdown!")
        os.system("sudo shutdown -h now")
        break
    time.sleep(1.0)
