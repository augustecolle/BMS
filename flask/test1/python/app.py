#!/usr/bin/env python

import os
os.chdir("/home/pi/spi_auguste/spi_can/flask/test1/python/")
import signal
from flask import Flask, request
from flask_restful import Resource, Api
import can_lib_auguste as au
import EAEL9080 as bb
import EAPSI8720 as au
import json
from RPi import GPIO
import ast
import time
import sqlite3 as lite
import sys
import subprocess
import numpy as np
import os

#au.startSerial('/dev/ttyUSB1')
time.sleep(0.1)
#au.remoteControllOn()
#au.readAndTreat()
#au.setCurrent(0)
#au.setVoltage(18)
#au.setPower(500)

bb.startSerial('/dev/ttyUSB0', "02")
time.sleep(0.1)
bb.setRemoteControllOn()
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
    print('Exiting program cleanly')
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
    #au.setVoltage(0)
    time.sleep(0.1)
    #au.setCurrent(0)
    time.sleep(0.1)
    #au.stopSerial()   
    time.sleep(0.1)
    for x in get_pid("python"):
        if (int(x) is not int(os.getpid())):
            os.kill(int(x), signal.SIGKILL)
    GPIO.cleanup()
    sys.exit(1)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def get_pid(name):
    return map(int, subprocess.check_output(["pidof", name]).split())

plogging = subprocess.Popen([sys.executable, './logging2db.py'])
time.sleep(2) #waiting for current calibration
#subprocess.Popen([sys.executable, './test.py'])

numslaves = 3 #link to database settings
con = None

app = Flask(__name__)
api = Api(app)

header = ["Timestamp", "Current", "MVoltage", "Sl1Voltage", "Sl2Voltage", "Sl3Voltage", "Sl4Voltage", "Sl5Voltage", "Sl6Voltage", "Sl7Voltage", "Sl8Voltage", "Sl9Voltage", "Sl10Voltage", "Sl11Voltage", "Sl12Voltage", "Sl13Voltage", "Sl14Voltage", "Sl15Voltage"]
global cut_off_voltage_low
cut_off_voltage_low = 2.8
global cut_off_voltage_high
cut_off_voltage_high = 4.1

headerBl = ["MBl", "Sl1Bl", "Sl2Bl", "Sl3Bl", "Sl4Bl", "Sl5Bl", "Sl6Bl", "Sl7Bl", "Sl8Bl", "Sl9Bl", "Sl10Bl", "Sl11Bl", "Sl12Bl", "Sl13Bl", "Sl14Bl", "Sl15Bl"]

bldict = {key:value for (key, value) in zip(headerBl, [0]*len(headerBl))}

class ActualValues(Resource):
    global cut_off_voltage_low
    global cut_off_voltage_high
    def get(self):
        dict = {}
        con = lite.connect('/home/pi/spi_auguste/spi_can/flask/test1/python/sqlite/test.db', timeout = 5.0)
        with con:
            cur = con.cursor()
            cur.execute("select * from MostRecentMeasurement")
            row = cur.fetchone()
        if con: con.close()
        for x in range(0, numslaves + 3):
            if header[x] is not "Current" and header[x] is not "Timestamp":
                volts = np.round(row[x], 5)
                print(header[x])
                print(volts)
                if (volts < cut_off_voltage_low):
                    print("CUT-OFF VOLTAGE LOW REACHED, SHUTTING DOWN EVERYTHING")
                    self.quit()
                    sys.exit(1)
                elif (volts > cut_off_voltage_high):
                    print("CUT-OFF VOLTAGE HIGH REACHED, SHUTTING DOWN EVERYTHING")
                    self.quit()
                    sys.exit(1)
                dict[header[x]] = volts
            else:
                dict[header[x]] = np.round(row[x], 2)
        return dict

    def quit(self):
        os.kill(int(os.getpid()), signal.SIGTERM)


class BleedingControll(Resource):
    def get(self, slave_id):
        return bldict[slave_id]

    def put(self, slave_id):
        bldict[slave_id] = 1 if (slave_id[-2:].lower() == 'on') else 0
        return bldict[slave_id]

class write2db(Resource):
    try:
        con = lite.connect('./sqlite/test.db')
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



