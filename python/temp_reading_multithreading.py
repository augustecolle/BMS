#!/usr/bin/python

import os
import glob
import time
import subprocess
import threading
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')

global lines
lines = []
#intervalMeasurement = 1.5 #in seconds

def getTempFromSingleDevice(file):
    global lines
    device_file = file + '/w1_slave'
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines.append(out_decode.split('\n'))

def read_temp_raw():
    global lines
    lines = []
    for file in device_folder:
        t = threading.Thread(target = getTempFromSingleDevice, args = (file,))
        t.start()
    return 0

def read_temp():
    global lines
    temps = []
    for line in lines:
        equals_pos = line[1].find('t=')
        if equals_pos != -1:
            temp_string = line[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
            temps.append(temp_c)
    lines = []
    return temps

if (__name__ == "__main__"):
    lastTime = time.time()
    while True:
        startTime = time.time()
        read_temp_raw()
        time.sleep(1.1) #have to wait this long or I get missing temperatures
        lastTime = startTime

