import os.path
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS

from common import PG_Orders, Order


app = fl.Flask(__name__)
CORS(app)


@app.route('/api/polus/orders/', methods=['POST', 'GET'])
def orders():
    if fl.request.method == 'POST':
        raw_order = Order.from_json(fl.request.json)
        order_id = PG_Orders.insert(raw_order)
        new_order = PG_Orders.get(order_id)
        return new_order.to_json()
    if fl.request.method == 'GET':
        driver_phone = fl.request.args.get('driver_phone')
        user_phone = fl.request.args.get('user_phone')
        orders = PG_Orders.get_list(driver_phone, user_phone)
        return [o.to_json() for o in orders]
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
