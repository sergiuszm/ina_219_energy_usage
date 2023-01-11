import RPi.GPIO as GPIO
import time

PIN = 21

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.HIGH)
    print('Led enabled!')
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.output(PIN, GPIO.LOW)
    print('Led disabled!')
    GPIO.cleanup()
