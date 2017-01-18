#!/usr/bin/env python

import os
import logging
import logconf
import logging.config
import signal
from flask import Flask, request
from flask_restful import Resource, Api
from libraries import can_lib_auguste as au
from libraries import EAEL9080 as bb
from libraries import EAPSI8720 as au
import json
from RPi import GPIO
import ast
import time
import sqlite3 as lite
import sys
import subprocess
import numpy as np
import psutil
import tempconf

logging.config.dictConfig(logconf.LOGGING)
global logger
logger = logging.getLogger('app')
 
au.startSerial('/dev/ttyUSB1')
time.sleep(0.1)
au.remoteControllOn()
au.readAndTreat()
au.setCurrent(0)
au.setVoltage(18)
au.setPower(500)

bb.startSerial('/dev/ttyUSB0', "02")
bb.setRemoteControllOn()
time.sleep(0.1)
bb.readAndTreat()
bb.readAndTreat()
bb.setInputOn()
bb.setCCMode()
bb.clearBuffer()
bb.setPowerA(1000)
bb.setVoltageA(17)
bb.setCurrentA(0)
bb.clearBuffer()

def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
def signal_handler(signal_s, frame):
    logger.critical('EXITING SYSTEM')
    time.sleep(0.1)
    bb.setCurrentA(0)
    time.sleep(0.1)
    bb.setVoltageA(0)
    time.sleep(0.5)
    bb.setPowerA(0)
    time.sleep(0.1)
    bb.setInputOff()
    time.sleep(0.1)
    bb.setRemoteControllOff()
    time.sleep(0.1)
    bb.stopSerial()
    time.sleep(0.1)
    au.setVoltage(0)
    time.sleep(0.1)
    au.setCurrent(0)
    time.sleep(0.1)
    au.stopSerial()   
    time.sleep(0.1)
    for x in get_pid("python"):
        process = psutil.Process(int(x))
        logger.debug("FOUND PYTHON PROCESS WITH ID: %d IN SIGNAL HANDLER OF APP.PY", x)
        logger.debug("Content of process.cmdline(): %s", process.cmdline())
        if (int(x) != int(os.getpid()) and process.cmdline() != [] and 'test' in process.cmdline()[1]):
            os.kill(int(x), signal.SIGTERM)
    GPIO.cleanup()
    sys.exit(1)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def get_pid(name):
    return map(int, subprocess.check_output(["pidof", name]).split())

#plogging = subprocess.Popen([sys.executable, './logging2db.py'])
time.sleep(2) #waiting for current calibration

numslaves = 3 #link to database settings
con = None

app = Flask(__name__)
api = Api(app)

header = ["Timestamp", "Current", "MVoltage", "Sl1Voltage", "Sl2Voltage", "Sl3Voltage", "Sl4Voltage", "Sl5Voltage", "Sl6Voltage", "Sl7Voltage", "Sl8Voltage", "Sl9Voltage", "Sl10Voltage", "Sl11Voltage", "Sl12Voltage", "Sl13Voltage", "Sl14Voltage", "Sl15Voltage"]
global cut_off_voltage_low
cut_off_voltage_low = 2.8
global cut_off_voltage_high
cut_off_voltage_high = 3.7

headerBl = ["MBl", "Sl1Bl", "Sl2Bl", "Sl3Bl", "Sl4Bl", "Sl5Bl", "Sl6Bl", "Sl7Bl", "Sl8Bl", "Sl9Bl", "Sl10Bl", "Sl11Bl", "Sl12Bl", "Sl13Bl", "Sl14Bl", "Sl15Bl"]

bldict = {key:value for (key, value) in zip(headerBl, [0]*len(headerBl))}

class ActualValues(Resource):
    global cut_off_voltage_low
    global cut_off_voltage_high
    global logger
    def get(self):
        dataDict = {}
        con = lite.connect('../database/test.db', timeout = 5.0)
        with con:
            cur = con.cursor()
            success = False
            while not success:
                try:
                    cur.execute("select * from MostRecentMeasurement")
                    success = True
                except:
                    time.sleep(0.01)
            row = cur.fetchone()
            colNames = list(map(lambda x: x[0], cur.description))
            dataDict = dict(zip(colNames, row))
            # map keys to their number of rings on the data cable
            for (key, val) in tempconf.tempmap.items():
                if key in dataDict:
                    dataDict[val] = dataDict.pop(key)
        if con: con.close()
        for x in dataDict.keys():
            if "Voltage" in x:
                dataDict[x] = round(dataDict[x], 5)
                print(round(dataDict[x], 5))
                #print(dataDict[x])
                if (dataDict[x] < cut_off_voltage_low):
                    logger.critical('UNDERVOLTAGE ON SLAVE %d REACHED, VOLTAGE NOW IS: %1.2f' % (x, volts))
                    self.quit()
                elif (dataDict[x] > cut_off_voltage_high):
                    logger.critical('OVERVOLTAGE ON SLAVE %d REACHED, VOLTAGE NOW IS: %1.2f' % (x, volts))
                    self.quit()
            else:
                dataDict[x] = round(dataDict[x], 2)
        print(dataDict)
        return dataDict

    def quit(self):
        for x in get_pid("python"):
            process = psutil.Process(int(x))
            logger.debug("FOUND PYTHON PROCESS WITH ID: %d", x)
            if (int(x) != int(os.getpid()) and ('test' in process.cmdline()[1])):
                os.kill(int(x), signal.SIGTERM)
                logger.debug("Sent SIGTERM to process ID: %d", int(x))
                time.sleep(0.5)
        #os.kill(int(os.getpid()), signal.SIGTERM)

class BleedingControll(Resource):
    def get(self, slave_id):
        return bldict[slave_id]

    def put(self, slave_id):
        bldict[slave_id] = 1 if (slave_id[-2:].lower() == 'on') else 0
        return bldict[slave_id]

class write2db(Resource):
    try:
        con = lite.connect('../database/test.db')
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print("SQLITE version: " + str(data))
    except lite.Error, e:
        print("Error " + str(e.args[0]))
        sys.exit(1)
    finally:
        if con:
            con.close()

    def get(self):
        pass


api.add_resource(ActualValues, '/ActualValues')
api.add_resource(write2db, '/write2db')
api.add_resource(BleedingControll, '/BleedingControll/<string:slave_id>')

#--- Enable CORS (cross origin requests), from: http://coalkids.github.io/flask-cors.html
@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers 
        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers
        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers 
    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:

        h['Access-Control-Allow-Origin'] = request.headers['Origin']
    return resp


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)



