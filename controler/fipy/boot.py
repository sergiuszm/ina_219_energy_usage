# boot.py -- run on boot-up
from machine import Pin
from pycom import rgbled, heartbeat

heartbeat(False)
rgbled(0x7f0000) # red
pin = Pin('P22', mode=Pin.IN, pull=Pin.PULL_DOWN)
