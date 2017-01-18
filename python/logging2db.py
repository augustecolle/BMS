#!/usr/bin/env python3

import os
import logging
import logconf
import logging.config
import signal
from libraries import can_lib_auguste as au
import temp_reading_multithreading as ds18b20
import time
import RPi.GPIO as GPIO
import sqlite3 as lite
import sys
import json

ds18b20.read_temp_raw() #start temperature conversion in sensors
tempinterval = 2

#import logger
logging.config.dictConfig(logconf.LOGGING)
logger = logging.getLogger('logging2db')

#setup signal handler
def signal_handler(signal_s, frame):
    logger.critical('EXITING LOGGING2DB')
    sys.exit(1)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

numslaves = 3 #link to database settings
loginterval = 1 #link to database settings
logging = 1 #link to database settings

tablestruct = ["Timestamp REAL", "Current REAL", "MVoltage REAL", "Sl1Voltage REAL", "Sl2Voltage REAL", "Sl3Voltage REAL", "Sl4Voltage REAL", "Sl5Voltage REAL", "Sl6Voltage REAL", "Sl7Voltage REAL", "Sl8Voltage REAL", "Sl9Voltage REAL", "Sl10Voltage REAL", "Sl11Voltage REAL", "Sl12Voltage REAL", "Sl13Voltage REAL", "Sl14Voltage REAL", "Sl15Voltage REAL"]
dbTable = "Timestamp REAL"

for x in range(1,numslaves+3):
    dbTable = dbTable + ", " + tablestruct[x]

for sensor in ds18b20.device_folder:
    print(sensor[-15:])
    dbTable = dbTable + ", " + "T" + sensor[-12:] + " REAL"


try:
    au.master_init()
    au.init_meting([i for i in range(1, numslaves+1)])
    au.currentCal(50)
    firstloop = 1
    count = 0
    tempcount = 0
    while True:
        con = lite.connect('../database/test.db', timeout = 5.0)
        with con:
            start = time.time()
            cur = con.cursor()
            voltageAll = au.getAll([x for x in range(1,numslaves+1)])
            voltagestr = str(time.time())
            #Only once in 2 measurements (2 seconds interval) because temp reading takes 1.1 seconds
            if (count % tempinterval == 0):
                tmp = ds18b20.read_temp()
                if(len(tmp) == 4):
                    templist = tmp
                    count = 0
                else:
                    logger.debug("only got %d values from tempsensors", len(tmp))
                ds18b20.read_temp_raw()
            for numslave in range(numslaves + 2):
                voltagestr = voltagestr + "," + str(voltageAll[numslave])
            for temp in templist:
                voltagestr = voltagestr + "," + str(temp)
            if (firstloop):
                cur.execute("DROP TABLE IF EXISTS Metingen")
                cur.execute("CREATE TABLE Metingen("+ dbTable +")")
                firstloop = 0
            cur.execute("DROP TABLE IF EXISTS MostRecentMeasurement")
            cur.execute("CREATE TABLE MostRecentMeasurement("+ dbTable +")")
            cur.execute("INSERT INTO Metingen VALUES("+voltagestr+")")
            cur.execute("INSERT INTO MostRecentMeasurement VALUES("+voltagestr+")")
        sltime = loginterval - (time.time() - start)
        con.close()
        count = count + 1
        if (sltime > 0 and sltime < 0.9): time.sleep(sltime)
except lite.Error as e:
    logger.debug("An error occurred: " + e.args[0])
except:
    GPIO.cleanup()
    print(sys.exc_info()[0])
    sys.exit(0)
