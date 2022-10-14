import flask as fl
from common import Order


app = fl.Flask(__name__)


@app.route('/orders/', methods=['POST'])
def orders():
    return fl.Response(status=201)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
