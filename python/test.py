#!/usr/bin/env python

import os
import logging
import logconf
import logging.config
import signal
from libraries import EAEL9080 as bb
from libraries import EAPSI8720 as au
import math
import csv
import numpy as np
import time as tm
import sys

logging.config.dictConfig(logconf.LOGGING)
logger_test = logging.getLogger('test')
 
#set signal handler
def signal_handler(signal, frame):
    logger_test.critical('EXITING TEST SCRIPT')
    bb.setCurrentA(0)
    bb.setVoltageA(0)
    #bb.setPowerA(0) #takes too long
    bb.setInputOff()
    bb.setRemoteControllOff()
    bb.stopSerial()
    au.setVoltage(0)
    au.setCurrent(0)
    au.stopSerial()   

#on kill and interrupt execute the signal_handler
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

#imp.reload(bb)
bb.startSerial('/dev/ttyUSB0', "02")
bb.setRemoteControllOn()
bb.setInputOn()
bb.setCCMode()
bb.setPowerA(1000)
bb.setVoltageA(17)
bb.setCurrentA(0)
bb.clearBuffer()


tm.sleep(1)

au.startSerial('/dev/ttyUSB1')
au.remoteControllOn()
au.readAndTreat()
#au.setCurrent(0)
au.setVoltage(16)
au.setPower(500)

tm.sleep(1)
#
try:
    while True:
        logger_test.debug("NEW TEST LOOP")
        au.setCurrent(3)
        tm.sleep(20*60)
        au.setCurrent(0)
        tm.sleep(3*60*60)
except:
    logger_test.debug("Exception occured")
    #bb.setCurrentA(0)
    #bb.setVoltageA(0)
    ##bb.setPowerA(0) #takes too long
    #bb.setInputOff()
    #bb.setRemoteControllOff()
    #au.setVoltage(0)
    #au.setCurrent(0)
    #bb.stopSerial()
    #au.stopSerial()   
    #sys.exit(1)

