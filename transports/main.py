import os.path
import sys
import datetime as dt

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS
from common import PG_Transports, PG_Orders, Transport


app = fl.Flask(__name__)
CORS(app)


def is_available_transport(start: dt.datetime, end: dt.datetime, transport: Transport) -> Transport:
    orders = PG_Orders.get_list(transport_type=transport.type, start=start, end=end)
    count = transport.amount
    events = []
    for order in orders:
        events.append(('start', order.start))
        events.append(('end', order.end))

    for e in sorted(events, key=lambda p: (p[1], 0 if p[0] == 'start' else 1)):
        if e[0] == 'start':
            count -= 1
        if e[0] == 'end':
            count += 1
        if count <= 0:
            break
    transport.amount = count
    return transport


@app.route('/api/polus/transports/', methods=['GET'])
def transports():
    if fl.request.method == 'GET':
        return [t.to_json() for t in PG_Transports.get_list()]
    return {}


@app.route('/api/polus/transports/available/', methods=['GET'])
def available():
    start = dt.datetime.fromisoformat(fl.request.args.get('start')) if fl.request.args.get('start') else None
    end = dt.datetime.fromisoformat(fl.request.args.get('end')) if fl.request.args.get('end') else None
    transport_type = fl.request.args.get('transport_type', '')
    transport = PG_Transports.get(transport_type)

    if any([start, end, transport]) and not all([start, end, transport]):
        return fl.Response(status=400)
    if all([start, end, transport]):
        if is_available_transport(start, end, transport).amount > 0:
            return [transport.to_json()]
        else:
            return []

    transports = PG_Transports.get_list()
    start = dt.datetime.now()
    end = start + dt.timedelta(hours=1)
    available_transports = []
    for transport in transports:
        available_transport = is_available_transport(start, end, transport)
        if available_transport.amount > 0:
            available_transports.append(transport)
    return [t.to_json() for t in available_transports]


@app.route('/api/polus/transports/<transport_type>', methods=['GET'])
def single_transport(transport_type):
    if fl.request.method == 'GET':
        transport = PG_Transports.get(transport_type=transport_type)
        return transport.to_json() if transport else fl.Response(status=404)
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
