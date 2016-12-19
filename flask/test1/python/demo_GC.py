import EAEL9080 as bb
import EAPSI8720 as au
import math
import csv
import numpy as np
import time as tm
import signal
import sys

#set signal handler
def signal_handler(signal, frame):
    print('Exiting program cleanly')
    tm.sleep(0.1)
    bb.setCurrentA(0)
    tm.sleep(0.1)
    bb.setVoltageA(0)
    tm.sleep(0.1)
    bb.setPowerA(0)
    tm.sleep(0.1)
    bb.setInputOff()
    tm.sleep(0.1)
    bb.setRemoteControllOff()
    tm.sleep(0.1)
    bb.stopSerial()
    tm.sleep(0.1)
    au.setVoltage(0)
    tm.sleep(0.1)
    au.setCurrent(0)
    tm.sleep(0.1)
    au.stopSerial()   
    tm.sleep(0.1)

#on kill and interrupt execute the signal_handler
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

au.startSerial()
au.remoteControllOn()
au.readAndTreat()
au.setCurrent(0)
au.setVoltage(18)
au.setPower(500)

bb.startSerial('/dev/ttyUSB1', "02")
bb.setRemoteControllOn()
bb.setInputOn()
bb.setCCMode()
bb.setPowerA(1000)
bb.setVoltageA(17)
bb.setCurrentA(0)
bb.clearBuffer()

try:
    while True:
        bb.setCurrentA(15)
        tm.sleep(20*60)
        bb.setCurrentA(0)
        tm.sleep(3*60*60)
except:
    bb.setCurrentA(0)
    bb.setVoltageA(0)
    bb.setPowerA(0)
    bb.setInputOff()
    bb.setRemoteControllOff()
    bb.stopSerial()
    au.setVoltage(0)
    au.setCurrent(0)
    au.stopSerial()   

#normally never gets here
print("DONE")



