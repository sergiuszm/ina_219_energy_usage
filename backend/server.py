#!/usr/bin/env python3
import socket
import netifaces as ni

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

ni.ifaddresses('wlp2s0')
ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                break