#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api
import can_lib_auguste as au
import json
import ast
import time
import sqlite3 as lite
import sys
import subprocess
import os
import numpy as np

numslaves = 4 #link to database settings
con = None

app = Flask(__name__)
api = Api(app)

p = subprocess.Popen([sys.executable, './logging2db.py'])

header = ["Timestamp", "Current", "MVoltage", "Sl1Voltage", "Sl2Voltage", "Sl3Voltage", "Sl4Voltage", "Sl5Voltage", "Sl6Voltage", "Sl7Voltage", "Sl8Voltage", "Sl9Voltage", "Sl10Voltage", "Sl11Voltage", "Sl12Voltage", "Sl13Voltage", "Sl14Voltage", "Sl15Voltage"]

headerBl = ["MBl", "Sl1Bl", "Sl2Bl", "Sl3Bl", "Sl4Bl", "Sl5Bl", "Sl6Bl", "Sl7Bl", "Sl8Bl", "Sl9Bl", "Sl10Bl", "Sl11Bl", "Sl12Bl", "Sl13Bl", "Sl14Bl", "Sl15Bl"]

bldict = {key:value for (key, value) in zip(headerBl, [0]*len(headerBl))}

class ActualValues(Resource):
    def get(self):
        dict = {}
        con = lite.connect('/home/pi/spi_auguste/spi_can/flask/test1/python/sqlite/test.db', timeout = 5.0)
        with con:
            cur = con.cursor()
            #cur.execute("select * from Metingen where Timestamp = (select max(Timestamp) from Metingen)")
            #cur.execute("select * from MostRecentMeasurement order by Timestamp desc limit 1")
            cur.execute("select * from MostRecentMeasurement")
            row = cur.fetchone()
        if con: con.close()
        print(row)
        for x in range(0, numslaves + 3):
            if header[x] is not "Current":
                dict[header[x]] = np.round(row[x], 5)
            else:
                dict[header[x]] = np.round(row[x], 2)
        return dict

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

