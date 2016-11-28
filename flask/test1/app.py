#!/usr/bin/env python2.7

from flask import Flask, request
from flask_restful import Resource, Api
import can_lib_auguste as au
import json
import ast
import time

app = Flask(__name__)
api = Api(app)

class ActualValues(Resource):
    au.master_init()
    def get(self):
        au.init_meting([0x01, 0x02, 0x03])
        au.getVoltageMaster()
        au.getCurrent()
        au.datadict['timestamp'].append(time.time())
        au.getVoltageSlaves([0x01, 0x02, 0x03])
        time.sleep(0.15)
        return json.dumps(au.datadict)


api.add_resource(ActualValues, '/ActualValues')


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
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)

