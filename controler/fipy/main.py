# main.py -- put your code here!
from network import WLAN
from machine import I2C, Pin, RTC, SD, unique_id, idle
from ina219 import INA219
import usocket as socket
import ujson
import utime
from pycom import rgbled
from os import mount, listdir, mkdir
from lcd import LCD, isConnected as lcdIsConnected
from ubinascii import hexlify
from urtc import DS3231, isConnected as rtcIsConnected

SHUNT_OHMS = 0.1
wlan = WLAN(mode=WLAN.STA)
WIFI_TO_CONNECT = ['cpsl']
MAX_LCD_POS = 7
LCD_DISPLAY = False
LCD_POS = -1


def get_wifi_cache():
    data = None
    try:
        f = open('/flash/wifi.json', 'r')
        data = f.readall()
        f.close()

    except OSError:
        log('No cache for WiFi!')
    
    try:
        if data is not None:
            cache = ujson.loads(data)

            return cache
    except ValueError:
        log('Cache is corrupted!')

    nets = wlan.scan()
    data = {}
    for net in nets:
        if net.ssid in WIFI_TO_CONNECT:
            data[net.ssid] = net.sec

    f = open('/flash/wifi.json', 'w+')
    log('Saving cache!')
    data = ujson.dumps(data)
    f.write(data)
    f.close()

    return data
    

def wifi_connect():
    nets = get_wifi_cache()
    for net in nets:
        if net in WIFI_TO_CONNECT:
            log('Network found!')
            wlan.connect(net, auth=(nets[net], 'quadflawhoAxslope9245'), timeout=5000)
            while not wlan.isconnected():
                idle() # save power while waiting
            log('Connected to WiFi!')
            # rgbled(0x007f00)
            break

def setup_rtc_from_ntp():
    rtc = RTC(id=0)
    rtc.ntp_sync("0.no.pool.ntp.org")
    utime.sleep_ms(750)
    # utime.timezone(3600)

    return rtc

def setup_rtc_from_ds3231():
    i2c = I2C(0, I2C.MASTER, baudrate=100000)
    if rtcIsConnected(i2c) is False:
        error = "DS3231 not detected!"
        log(error)
        raise OSError(error)    
        
    ds3231 = DS3231(i2c)
    rtc = RTC(id=0)
    dt = ds3231.datetime()
    rtc.init((dt[0], dt[1], dt[2], dt[4], dt[5], dt[6], 0, 0))
    utime.sleep_ms(750)

    return rtc

def send_data(data):
    sockaddr = socket.getaddrinfo('lmi034-1.cpsl.lan', 65432)[0][-1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(True)
    s.connect(sockaddr)
    json = ujson.dumps(data)    
    s.sendall(json.encode())
    s.close()                   

def configure_ina219():
    i2c = I2C(0, I2C.MASTER, baudrate=100000)
    devices = i2c.scan()

    if INA219.__ADDRESS not in devices:
        log('No INA219 detected!')
        
        return None
    
    log('INA219 found!')
    ina = INA219(SHUNT_OHMS, i2c, max_expected_amps=1.0)
    ina.configure(voltage_range=INA219.RANGE_16V, bus_adc=INA219.ADC_4SAMP)

    return ina

def read_ina219():
    timestamp = utime.mktime(utime.localtime())
    current = ina.current()
    voltage = ina.voltage()
    power1 = ina.power()
    power2 = current * voltage
    
    # print("%.3f | %.3f | %.3f | %.3f" % (current, voltage, power2, power1))
    return "%d | %.3f | %.3f | %.3f | %.3f" % (timestamp, current, voltage, power1, power2)
    # return "%.3f | %.3f" % (current, voltage)


def get_f_time():
    def _format(time_part):
        time_part = time_part if time_part >= 10 else "0{}".format(time_part)
        return time_part

    date = utime.gmtime()
    year = date[0]
    month = _format(date[1])
    day = _format(date[2])
    hour = _format(date[3])
    minute = _format(date[4])
    second = _format(date[5])
    d_time = "{}-{}-{}".format(year, month, day)
    h_time = "{}:{}:{}".format(hour, minute, second)

    return d_time, h_time

def prepare_sd():
    global EXP_NR, DEVICE
    try:
        sd = SD()
    except OSError:
        log('No SD card found!')
        return False

    try:
        mount(sd, '/sd')
    except OSError:
        log('Can\'t mount SD!')
        return False
    
    dirs = listdir('/sd')
    has_data_dir = False
    for d in dirs:
        if 'data' == d:
            has_data_dir = True
            log('Found data dir!')
            break

    if has_data_dir is False:
        mkdir('/sd/data')

    try:
        f_time, _ = get_f_time()
        f = open('/sd/data/info-ina219-{}-{}'.format(DEVICE, f_time), 'r')
        lines = f.readall()
        f.close()

        if len(lines) == 0:
            EXP_NR = 0

        if len(lines) > 0:
            EXP_NR = lines.count('#')
    except OSError:
        log('Creating new info!')
        f = open('/sd/data/info-ina219-{}-{}'.format(DEVICE, f_time), 'w+')
        f.close()
        EXP_NR = 0

    log("Next experiment: #{}".format(EXP_NR))
    return True


def save_data(readings):
    global EXP_NR, SD_CARD, DEVICE
    if len(readings) == 0:
        return

    rgbled(0x7f7f00)
    if SD_CARD:
        log('#{}: Saving data|SD'.format(EXP_NR))
        f_time, _ = get_f_time()
        f = open('/sd/data/info-ina219-{}-{}'.format(DEVICE, f_time), 'a+')
        f.write("#{}\n".format(EXP_NR))
        f.close()

        f = open('/sd/data/ina219-{}-{}-{}'.format(DEVICE, f_time, EXP_NR), 'a+')
        for line in readings:
            line = "{}\n".format(line)
            f.write(line)

        f.close()
        log('#{}: Data saved|SD!'.format(EXP_NR))
        return

    log('#{}: Sending data|WiFi'.format(EXP_NR))
    send_data(readings)
    log('#{}: Data sent|WiFi'.format(EXP_NR))
    rgbled(0x007f00) # green

def init_lcd():
    global LCD_DISPLAY, lcd
    i2c = I2C(0, I2C.MASTER, baudrate=100000)

    if lcdIsConnected(i2c):
        LCD_DISPLAY = True
        lcd = LCD(i2c)
        # lcd.initialize(i2c, lcd.kDisplayI2C128x64)
        lcd.set_contrast(128) # 1-255
        lcd.displayOn()
        lcd.clearBuffer()
        lcd.drawBuffer()

        return

def log(text):
    global LCD_POS, LCD_DISPLAY, lcd
    if LCD_DISPLAY is True:
        LCD_POS += 1
        if LCD_POS > 7:
            LCD_POS = 0
            lcd.clearBuffer()

        lcd.addString(0, LCD_POS, text)
        lcd.drawBuffer()
    
    print(text)

def assign_device_name():
    global DEVICE
    dev_id = hexlify(unique_id()).decode()
    data = None
    try:
        f = open('/flash/device.json', 'r')
        data = f.readall()
        f.close()
    except OSError:
        log('No device.json!')
    
    try:
        if data is not None:
            cache = ujson.loads(data)
    except ValueError:
        log('Device file is corrupted!')

    try:
        DEVICE = cache[dev_id]
    except KeyError:
        log('Device name missing:')
        log(dev_id)

        raise OSError('Device name missing!')

    log("Host: {}".format(DEVICE))

if __name__ == '__main__':
    pin = Pin('P22', mode=Pin.IN, pull=Pin.PULL_DOWN)
    rgbled(0x7f0000) # red

    global EXP_NR, SD_CARD, DEVICE
    EXP_NR = 0

    init_lcd()
    assign_device_name()
    # wlan_ip = wlan.ifconfig()
    # if wlan_ip[0] == '0.0.0.0':
    #     wifi_connect()
    #     wlan_ip = wlan.ifconfig()
    
    # log("IP: {}".format(wlan_ip[0]))

    rtc = setup_rtc_from_ds3231()
    f_time, h_time = get_f_time()
    log("{} {}".format(f_time, h_time))
    ina = configure_ina219()

    SD_CARD = prepare_sd()
    if SD_CARD is False:
        for x in range(0, 5):
            rgbled(0x7f0000) # red
            utime.sleep_ms(500)
            rgbled(0xff00ff) # magneta
            utime.sleep_ms(500)

    if ina is not None:
        rgbled(0x007f00) # green
        readings = []
        prev_pin_val = pin.value()

        while True:
            pin_val = pin.value()
            
            if prev_pin_val != pin_val: 
                if pin_val == 1:
                    log('#{}: Exp started!'.format(EXP_NR))
                    rgbled(0x0000ff) # blue
                    readings = []
                    if SD_CARD is False:
                        readings.append(DEVICE)
                    # READINGS.append(DEVICE)
                else:
                    log('#{}: Exp ended!'.format(EXP_NR))
                    save_data(readings)
                    rgbled(0x007f00) # green
                    EXP_NR += 1
                    log('Next experiment: #{}'.format(EXP_NR))

            if pin_val == 1:
                readings.append(read_ina219())
                utime.sleep_ms(200)

            prev_pin_val = pin_val        

    rgbled(0x7f0000) # red