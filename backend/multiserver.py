#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import netifaces as ni
import json
import os.path
import datetime

sel = selectors.DefaultSelector()

PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# ni.ifaddresses('eno1')
HOST = ni.ifaddresses('eno1')[ni.AF_INET][0]['addr']
path = "/home/lmi034/master-election-data/"

MIN_SAMPLE = 1

def file_len(name):
    with open(name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def save_to_file(filename, data):
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path + filename
    with open(filename, 'a') as out:
        out.write(str(data) + '\n')

def get_time():
    time_object = datetime.datetime.now()
    date_time = time_object.strftime("%Y-%m-%d %H:%M:%S")
    date = time_object.strftime("%Y-%m-%d")
    timestamp = int(time_object.timestamp())

    return date_time, date, timestamp

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
            buff = json.loads(data.outb)

            if len(buff) >= MIN_SAMPLE:
                _, date, _ = get_time()
                device = buff[0]
                buff = buff[1:]
                info_filename = "info-ina219-{}-{}".format(device, date)

                experiment_nr = 0
                if os.path.isfile(path + info_filename):
                    experiment_nr = file_len(path + info_filename)

                save_to_file(info_filename, "#{}".format(experiment_nr))
                
                ina2019_filename = "ina219-{}-{}-{}".format(device, date, experiment_nr)
                for x in buff:
                    save_to_file(ina2019_filename, x)
                    print(x)


if __name__ == '__main__':
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print("listening on", (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()
