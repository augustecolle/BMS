from flask import Flask, request, Response
from flask_restful import reqparse, abort, Api, Resource
from main_get import *
from constants import *
from getCron import *
from temperatuur import *
from restartModule import *
import glob
import os
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('logInterval')
parser.add_argument('sendInterval')

class getMeter(Resource):
    def get(self, meter_id):
        data = getModbusData(meter_id)
        #response = make_response(data,200)
        #response.headers['content-type'] = 'application/octet-stream'
        return data

class getDS18B20(Resource):
    def get(self):
        base_dir = "/sys/bus/w1/devices/"
        path = glob.glob(base_dir + '28*')
	address = {'address':[]}
        for i in range(0,len(path)):
            address['address'].append(os.path.split(path[i])[1])
        return address

class interval(Resource):
    def post(self):
	args = parser.parse_args()
	logInterval = args["logInterval"]
	sendInterval = args["sendInterval"]
	res = os.system(pathPython + " " + pathSetCron + " "  + logInterval + " " + sendInterval)
	if res == 0: temp = {'result':'success'}
	else: temp = {'result':'failed'}
	return temp
    def get(self):
	return getCron()

class changeTI(Resource):
    def post(self):
	res = os.system(pathTI)
	#nakijken als er hier nog een controle kan uitgevoerd worden
	return res

class getTemperature(Resource):
    def get(self, address):
	return {'temperature':getTemp(address)}

class restartPulse(Resource):
    def post(self):
	restartPythonPulse()
	return "ok"

api.add_resource(getMeter, '/meter/<meter_id>/')
api.add_resource(getDS18B20, '/tempSensor/')
api.add_resource(getTemperature, '/getTemperature/<address>/')
api.add_resource(interval, '/interval/')
api.add_resource(changeTI, '/changeTI/')
api.add_resource(restartPulse, '/restartPulse/')

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
    app.run(debug=True, host="0.0.0.0", port=8080, threaded=True)

