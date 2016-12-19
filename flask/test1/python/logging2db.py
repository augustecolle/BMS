#!/usr/bin/env python


import os
os.chdir("/home/pi/spi_auguste/spi_can/flask/test1/python/")

import can_lib_auguste as au
import time
import RPi.GPIO as GPIO
import sqlite3 as lite
import sys
import json
import imp
imp.reload(au)

numslaves = 4 #link to database settings
loginterval = 1 #link to database settings
logging = 1 #link to database settings

tablestruct = ["Timestamp REAL", "Current REAL", "MVoltage REAL", "Sl1Voltage REAL", "Sl2Voltage REAL", "Sl3Voltage REAL", "Sl4Voltage REAL", "Sl5Voltage REAL", "Sl6Voltage REAL", "Sl7Voltage REAL", "Sl8Voltage REAL", "Sl9Voltage REAL", "Sl10Voltage REAL", "Sl11Voltage REAL", "Sl12Voltage REAL", "Sl13Voltage REAL", "Sl14Voltage REAL", "Sl15Voltage REAL"]
dbTable = "Timestamp REAL"

for x in range(1,numslaves+3):
    dbTable = dbTable + ", " + tablestruct[x]

try:
    au.master_init()
    au.init_meting([i for i in range(1, numslaves+1)])
    au.currentCal(50)
    firstloop = 1

    while True:
        con = lite.connect('./sqlite/test.db')
        with con:
            start = time.time()
            cur = con.cursor()
            voltageAll = au.getAll([x for x in range(1,numslaves+1)])
            voltagestr = str(time.time())
            for numslave in range(numslaves + 2):
                voltagestr = voltagestr + "," + str(voltageAll[numslave])
            if (not logging or firstloop):
                cur.execute("DROP TABLE IF EXISTS Metingen")
                cur.execute("CREATE TABLE Metingen("+ dbTable +")")
                firstloop = 0
            cur.execute("DROP TABLE IF EXISTS MostRecentMeasurement")
            cur.execute("CREATE TABLE MostRecentMeasurement("+ dbTable +")")
            cur.execute("INSERT INTO Metingen VALUES("+voltagestr+")")
            cur.execute("INSERT INTO MostRecentMeasurement VALUES("+voltagestr+")")
        sltime = loginterval - (time.time() - start)
        con.close()
        if (sltime > 0 and sltime < 0.9): time.sleep(sltime)
except:
    GPIO.cleanup()
    print(sys.exc_info()[0])
    sys.exit(0)
