import os.path
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS


app = fl.Flask(__name__)
CORS(app)


@app.route('/api/polus/drivers/', methods=['GET'])
def drivers():
    if fl.request.method == 'GET':
        return []
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082)
