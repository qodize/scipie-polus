import os.path
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from common import Order


app = fl.Flask(__name__)


@app.route('/api/polus/orders', methods=['POST'])
def orders():
    return fl.Response(status=201)


@app.route('/api/polus/orders', methods=['GET'])
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
