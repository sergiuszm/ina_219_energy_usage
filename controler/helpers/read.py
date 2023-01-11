import serial
from time import sleep
import os.path
import datetime
import psutil
import RPi.GPIO as GPIO
import argparse
import socket

path = "/home/pi/data/power/"

def read_current_and_voltage(): 
    with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:

        try:
            line = ser.readline()
            if len(line) > 0:
                decoded_line = line.decode('utf-8')
                decoded_line = decoded_line.replace('\r\n', '')
                
                return decoded_line
        except serial.serialutil.SerialException:
            return None

def file_len(name):
    count = 0
    with open(name) as f:
        count = len(f.readlines())
    print(count)
    return count

def save_to_file(file_name, timestamp, data):
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + file_name
    with open(filename, 'a') as out:
        out.write("{} | ".format(timestamp) + str(data) + '\n')

def get_time():
    time_object = datetime.datetime.now()
    date_time = time_object.strftime("%Y-%m-%d %H:%M:%S")
    date = time_object.strftime("%Y-%m-%d")
    timestamp = int(time_object.timestamp())

    return date_time, date, timestamp


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Experiment")
    parser.add_argument('count', type=int, help='Number of the experiment')
    
    args = parser.parse_args()
    experiment_nr = args.count
    _, date, _ = get_time()
    hostname = socket.gethostname()
    file_name = "sleepypi2-{}-{}-{}".format(hostname, date, experiment_nr)

    try:
        while True:
            _, _, timestamp = get_time()
            
            values = read_current_and_voltage()
            if values is not None:
                save_to_file(file_name, timestamp, values)
    
    except KeyboardInterrupt:
        while values is not None:
            values = read_current_and_voltage()
            if values is not None:
                save_to_file(file_name, timestamp, values)
        # values = read_current_and_voltage()
