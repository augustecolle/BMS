import EAPSI8720 as au
import math
import numpy as np
import time as tm
import signal
import sys

def signal_handler(signal, frame):
    print('Exiting program cleanly')
    au.setVoltage(0)
    au.setCurrent(0)
    au.stopSerial()   

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

au.startSerial('/dev/ttyUSB1')
au.remoteControllOn()
au.readAndTreat()

logtime = 1 #seconds

cyclelog = 0

#Charge at  bulck charge untill battery voltage is 16V
au.setCurrent(15)
au.setVoltage(4*4)
au.setPower(400)
while(au.getActualValues()[0] < 4*4):
    start = tm.time()
    cyclelog += 1
    print("bulk charging, cyclelog: " + str(cyclelog))
    #wait till one second passed since beginning of cycle
    tm.sleep(logtime - (tm.time() - start))
        

#Absorption fase, charge at 16 untill current < 5A
begin = tm.time()
au.setVoltage(16.0)
while(au.getActualValues()[1] > (5)):
    start = tm.time()
    cyclelog += 1
    print("Absorption charging, cyclelog: " + str(cyclelog))
    #wait till one second passed since beginning of cycle
    tm.sleep(logtime - (tm.time() - start))

cyclelog = 0

au.setVoltage(0)
au.setCurrent(0)
au.stopSerial()
