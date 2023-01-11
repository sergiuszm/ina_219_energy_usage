from pyRpc import RpcConnection
import datetime
from time import sleep


class Logger:

    def __init__(self):
        self._remote = RpcConnection("pyLCD", workers=1)
        sleep(.1)

    def log(self, msg):
        print(msg)
        self._remote.call("log", args=[msg])


def get_date():
    time_object = datetime.datetime.now()
    date = time_object.strftime("%Y-%m-%d_%H%M%S")
    return date


def get_timestamp():
    time_object = datetime.datetime.now()
    return int(time_object.timestamp())
