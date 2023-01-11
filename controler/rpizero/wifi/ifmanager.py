import RPi.GPIO as GPIO
from rpizero.common import Logger
import subprocess
from time import sleep
import signal
import os
from rpizero.wifi.wificheck import get_status, STATUS_UP

PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
SERVER_P = None


def start_server():
    global SERVER_P
    SERVER_P = subprocess.Popen(["python3", "-m", "rpizero.wifi.file_server"])


def kill_server():
    global SERVER_P
    if SERVER_P.poll() is None:
        SERVER_P.send_signal(signal.SIGINT)
        SERVER_P.wait()
    SERVER_P = None


if __name__ == '__main__':
    logger = Logger()
    logger.log('IFMANAGER started!')

    wifi_status = get_status()
    if wifi_status == STATUS_UP:
        start_server()

    try:
        while True:
            wifi_status = get_status()
            if GPIO.input(PIN):
                if wifi_status == STATUS_UP:
                    logger.log("Disabling WiFi")
                    kill_server()
                    os.system("sudo ifconfig wlan0 down")
                else:
                    logger.log("Enabling WiFi")
                    os.system("sudo iwlist wlan0 scan")
                    os.system("sudo ifconfig wlan0 up")
                    start_server()

            sleep(2)

    except KeyboardInterrupt:
        if SERVER_P is not None:
            kill_server()
        logger.log('IFMANAGER killed!')
