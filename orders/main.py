import flask as fl
from common import Order


app = fl.Flask(__name__)


@app.route('/orders/', methods=['POST'])
def orders():
    return fl.Response(status=201)


@app.route('/')
def hello_world():
    return 'Hello, World!'
