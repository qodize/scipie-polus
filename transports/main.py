import os.path
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl


app = fl.Flask(__name__)


@app.route('/api/polus/transports/', methods=['GET'])
def orders():
    return [{'id': 0, 'type': 'Большая машина'}, {'id': 1, 'type': 'Машина поменьше'}, {'id': 2, 'type': 'Умная машина'}]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
