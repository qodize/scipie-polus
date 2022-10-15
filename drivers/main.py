import os.path
import sys
import datetime as dt

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import flask as fl
from flask_cors import CORS
from common import PG_Drivers, Driver


app = fl.Flask(__name__)
CORS(app)


@app.route('/api/polus/drivers/', methods=['GET', 'POST'])
def drivers():
    if fl.request.method == 'POST':
        data = fl.request.json
        driver = PG_Drivers.get_driver(data['phone_number'])
        if not driver:
            driver = Driver(None, data['phone_number'])
            driver_id = PG_Drivers.create_driver(driver)
        driver = PG_Drivers.get_driver(data['phone_number'])
        return driver.to_json()
    if fl.request.method == 'GET':
        return []
    return {}


@app.route('/api/polus/drivers/schedule/', methods=['GET'])
def all_schedules():
    if fl.request.method == 'GET':
        start = fl.request.args.get('start')
        end = fl.request.args.get('end')
        start = dt.datetime.fromisoformat(start) if start else None
        end = dt.datetime.fromisoformat(end) if end else None
        return [s.to_json() for s in PG_Drivers.get_schedule(start, end)]
    return {}


@app.route('/api/polus/drivers/schedule/<driver_phone>', methods=['GET'])
def driver_schedule(driver_phone):
    if fl.request.method == 'GET':
        return [s.to_json() for s in PG_Drivers.get_driver_schedule(driver_phone)]
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082)
