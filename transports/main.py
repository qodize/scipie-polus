import os.path
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS
from common import PG_Transports


app = fl.Flask(__name__)
CORS(app)


@app.route('/api/polus/transports/', methods=['GET'])
def transports():
    if fl.request.method == 'GET':
        return [t.to_json() for t in PG_Transports.get_list()]
    return {}


@app.route('/api/polus/transports/<transport_type>', method=['GET'])
def single_transport(transport_type):
    if fl.request.method == 'GET':
        return PG_Transports.get(transport_type=transport_type).to_json()
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
