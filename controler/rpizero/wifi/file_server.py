import http.server
import socketserver
import os
import zipfile
from rpizero.common import Logger, get_date
import shutil
import netifaces as ni
import socket

PORT = 8000
DATA_PATH = '/home/pi/data/power/'
WEB_DIR = '/home/pi/web/'
logger = Logger()


def _zipdir():
    logger.log('Compressing data')
    date_t = get_date()
    ziph = zipfile.ZipFile('{}{}_{}.zip'.format(WEB_DIR, socket.gethostname(), date_t), 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            ziph.write(os.path.join(root, file))

    ziph.close()
    logger.log('{}.zip'.format(date_t))


def _delete_data():
    logger.log('Deleting data')
    try:
        shutil.rmtree(DATA_PATH)
    except OSError as e:
        logger.log('Error!')
        print("Error: %s - %s." % (e.filename, e.strerror))
        return

    logger.log('Data removed')


def _wait_for_interface_up():
    ip = None
    while ip is None:
        try:
            ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        except KeyError:
            ip = None

    return ip


def zip_and_serve():
    try:
        files = os.listdir(DATA_PATH)
        if len(files) > 0:
            _zipdir()
            _delete_data()
            os.mkdir(DATA_PATH)

        ip = _wait_for_interface_up()

        logger.log('Starting web server')
        os.chdir(WEB_DIR)
        http_handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), http_handler)
        logger.log("{}:{}".format(ip, PORT))
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.log('Server killed!')


if __name__ == '__main__':
    zip_and_serve()
