import RPi.GPIO as GPIO
from time import sleep
import argparse
import os.path
import datetime
import subprocess
import signal
import socket

path = "/home/pi/data/power/"
EXP_PIN = 25

def file_len(name):
    with open(name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def save_to_file(name, data):
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + name
    with open(filename, 'a') as out:
        out.write(str(data) + '\n') 

def get_time():
    time_object = datetime.datetime.now()
    timestamp = time_object.strftime("%Y-%m-%d %H:%M:%S")
    date = time_object.strftime("%Y-%m-%d")
    return timestamp, date


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Experiment")
    parser.add_argument('name', help='Name of the experiment')

    print("Informing SleepyPi2 of the experiment!")
    args = parser.parse_args()
    timestamp, date = get_time()
    hostname = socket.gethostname()
    info_filename = "info-{}-{}".format(hostname, date)

    experiment_nr = 0
    if os.path.isfile(path + info_filename):
        experiment_nr = file_len(path + info_filename)

    save_to_file(info_filename, "#{}: {}".format(experiment_nr, args.name))

    p = subprocess.Popen(["python3", "read.py", str(experiment_nr)])

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EXP_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(EXP_PIN, GPIO.HIGH)

    try:
        while True:
            GPIO.output(EXP_PIN, GPIO.HIGH)
            sleep(0.1) 

    except KeyboardInterrupt:
        GPIO.output(EXP_PIN, GPIO.LOW)
        GPIO.cleanup()
        sleep(2)
        p.send_signal(signal.SIGINT)
        p.wait()
        print("Ending experiment.")
        # save_to_file(date, "#### END OF: {} ####\n".format(experiment_nr))
