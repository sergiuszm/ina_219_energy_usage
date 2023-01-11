import RPi.GPIO as GPIO
from time import sleep
import argparse
import os.path
import datetime
import subprocess
import signal
import socket

EXP_PIN = 25

if __name__ == "__main__":
    print("Starting experiment.")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EXP_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(EXP_PIN, GPIO.HIGH)

    try:
        while True:
            GPIO.output(EXP_PIN, GPIO.HIGH)
            sleep(0.5) 

    except KeyboardInterrupt:
        GPIO.output(EXP_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("Ending experiment.")
