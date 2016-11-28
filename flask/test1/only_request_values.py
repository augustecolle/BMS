#!/usr/bin/env python2.7

from flask import Flask, request
from flask_restful import Resource, Api
import can_lib_auguste as au
import time

app = Flask(__name__)
api = Api(app)

class voltageSlaves(Resource):
    au.master_init()
    def get(self):
        au.init_meting([0x01, 0x02, 0x03])
        au.getVoltageMaster()
        au.getCurrent()
        au.datadict['timestamp'].append(time.time())
        au.getVoltageSlaves([0x01, 0x02, 0x03])
        time.sleep(0.15)
        return au.datadict

api.add_resource(voltageSlaves, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
