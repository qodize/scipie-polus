import os.path
import sys
import datetime as dt
import requests

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS

from common import PG_Orders, Order, Transport, DriverSchedule


app = fl.Flask(__name__)
CORS(app)


def is_available_transport(start: dt.datetime, end: dt.datetime, transport: Transport) -> bool:
    orders = PG_Orders.get_list(transport_type=transport.type, start=start, end=end)
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
        return False
    return True


def find_available_driver(start: dt.datetime, end: dt.datetime) -> str or None:
    query = f'https://scipie.ru/api/polus/drivers/schedule/?start={start.isoformat()}&end={end.isoformat()}'
    schedules_res = requests.get(query)
    if schedules_res.status_code != 200:
        raise requests.HTTPError()

    schedules = [DriverSchedule.from_json(s) for s in schedules_res.json()]
    for schedule in schedules:
        orders = PG_Orders.get_list(driver_phone=schedule.driver_phone, start=schedule.start, end=schedule.end)
        for order in orders:
            if not (end < order.start or order.end < start):
                break
        else:
            return schedule.driver_phone
    return None


@app.route('/api/polus/orders/', methods=['GET', 'POST', 'PATCH'])
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
        start = new_order.start
        end = new_order.end
        while not (is_available := is_available_transport(start, end, transport)):
            start += dt.timedelta(minutes=30)
            end += dt.timedelta(minutes=30)

        if start != new_order.start:
            new_order.status = 'transport unavailable'
            PG_Orders.update(new_order)
            return {"order": new_order.to_json(),
                    'suggestion_start': start.isoformat(),
                    'suggestion_finish': end.isoformat()}
        try:
            start = new_order.start
            end = new_order.end
            border = start + dt.timedelta(hours=10)
            while not (driver_phone := find_available_driver(start, end)):
                start += dt.timedelta(minutes=30)
                end += dt.timedelta(minutes=30)
                if start >= border:
                    break
        except requests.HTTPError as e:
            print(f'SCHEDULES ERROR')
            new_order.status = "driver was not assigned"
            PG_Orders.update(new_order)
            return {'order': new_order.to_json()}

        if not driver_phone:
            new_order.status = "no available drivers"
            PG_Orders.update(new_order)
            return {'order': new_order.to_json()}
        elif start != new_order.start:
            new_order.status = "no available drivers"
            PG_Orders.update(new_order)
            return {'order': new_order.to_json(), 'suggestion_start': start, 'suggestion_end': end}

        new_order.status = "assigned"
        new_order.driver_phone = driver_phone
        PG_Orders.update(new_order)
        return {'order': new_order.to_json()}

    if fl.request.method == 'GET':
        driver_phone = fl.request.args.get('driver_phone')
        user_phone = fl.request.args.get('user_phone')
        orders = PG_Orders.get_list(driver_phone, user_phone)
        return [o.to_json() for o in orders]

    if fl.request.method == 'PATCH':
        data = fl.request.json
        order_id = data.get('id')
        status = data.get('status')
        if not status:
            return fl.Response(status=400)
        order = PG_Orders.get(order_id)
        order.status = status
        PG_Orders.update(order)
        return order.to_json()

    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
