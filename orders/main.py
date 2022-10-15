import os.path
import sys
import requests

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS

from common import PG_Orders, Order, Transport, DriverSchedule


app = fl.Flask(__name__)
CORS(app)


@app.route('/api/polus/orders/', methods=['POST', 'GET'])
def orders():
    if fl.request.method == 'POST':
        raw_order = Order.from_json(fl.request.json)
        query = 'https://' + requests.utils.quote(f'scipie.ru/api/polus/transports/{raw_order.transport_type}')
        transports_res = requests.get(query)

        if transports_res.status_code != 200:
            return fl.Response(raw_order.to_json(), 404)
        transport_json = transports_res.json()
        transport = Transport(**transport_json)

        order_id = PG_Orders.insert(raw_order)
        new_order = PG_Orders.get(order_id)
        orders = PG_Orders.get_list(transport_type=transport.type, start=new_order.start, end=new_order.end)
        count = transport.amount
        events = []
        for order in orders:
            events.append(('start', order.start))
            events.append(('end', order.end))

        for e in sorted(events, key=lambda p: p[1]):
            if e[1] == 'start':
                count -= 1
            if e[1] == 'end':
                count += 1
            if count <= 0:
                break

        if count <= 0:
            new_order.status = 'transport unavailable'
            PG_Orders.update(new_order)
            return new_order.to_json()

        query = 'https://' + requests.utils.quote(f'scipie.ru/api/polus/drivers/schedule/?start={new_order.start.isoformat()}&end={new_order.end.isoformat()}')
        schedules_res = requests.get(query)
        if schedules_res.status_code != 200:
            print(f'SCHEDULES ERROR {schedules_res.status_code=}')
            new_order.status = "driver was not assigned"
            PG_Orders.update(new_order)
            return new_order.to_json()

        schedules = [DriverSchedule(*s) for s in schedules_res.json()]
        for schedule in schedules:
            orders = PG_Orders.get_list(driver_phone=schedule.driver_phone, start=schedule.start, end=schedule.end)
            for order in orders:
                if not (new_order.end < order.start or order.end < new_order.start):
                    break
            else:
                new_order.driver_phone = schedule.driver_phone
                break

        if not new_order.driver_phone:
            print("NO AVAILABLE DRIVERS")
            new_order.status = "no available drivers"
            PG_Orders.update(new_order)
            return new_order.to_json()

        new_order.status = "assigned"
        PG_Orders.update(new_order)
        return new_order.to_json()

    if fl.request.method == 'GET':
        driver_phone = fl.request.args.get('driver_phone')
        user_phone = fl.request.args.get('user_phone')
        orders = PG_Orders.get_list(driver_phone, user_phone)
        return [o.to_json() for o in orders]
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
