import psycopg2
from .types import *
import datetime as dt
from typing import List

pg_database = 'polus'
pg_username = 'postgres'
pg_password = 'postgres'
pg_host = '127.0.0.1'


def postgres_wrapper(func):
    def wrap(*args, **kwargs):
        with psycopg2.connect(dbname=pg_database,
                              user=pg_username,
                              password=pg_password,
                              host=pg_host) as conn:
            with conn.cursor() as cursor:
                return func(cursor, *args, **kwargs)

    return wrap


class PG_Orders:
    @staticmethod
    @postgres_wrapper
    def insert(cursor, order: Order) -> int:
        cursor.execute(f"""INSERT INTO orders
         VALUES (DEFAULT,
                 '{order.user_phone}',
                 '{order.driver_phone if order.driver_phone else ""}',
                 '{order.transport_type}',
                 '{order.start}',
                 '{order.end}',
                 {order.latitude},
                 {order.longitude},
                 '{order.status}')
         RETURNING orders.id""")
        order_id = cursor.fetchall()[0][0]
        return order_id

    @staticmethod
    @postgres_wrapper
    def get(cursor, order_id: int) -> Order:
        cursor.execute(f"""SELECT * FROM orders WHERE id = {order_id}""")
        order = Order(*cursor.fetchall()[0])
        return order

    @staticmethod
    @postgres_wrapper
    def get_list(cursor, driver_phone=None, user_phone=None):
        query = f"""SELECT * FROM orders WHERE id >= 0"""
        if driver_phone:
            query += f" AND driver_phone like '{driver_phone}'"
        if user_phone:
            query += f" AND user_phone like '{user_phone}'"
        cursor.execute(query)
        return [Order(*o) for o in cursor.fetchall()]

    @staticmethod
    @postgres_wrapper
    def create_table(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
        id serial PRIMARY KEY,
        user_phone varchar(100),
        driver_phone varchar(100),
        transport_type varchar(100),
        dtstart timestamp,
        dtend timestamp,
        latitude float,
        longitude float,
        status varchar(100)
        )""")


class PG_Transports:
    @staticmethod
    @postgres_wrapper
    def get_list(cursor):
        cursor.execute(f"""SELECT * FROM transports""")
        return [Transport(*t) for t in cursor.fetchall()]


class PG_Drivers:
    @staticmethod
    @postgres_wrapper
    def get_driver_list(cursor):
        cursor.execute(f"""SELECT * FROM drivers""")
        return [Driver(*d) for d in cursor.fetchall()]

    @staticmethod
    @postgres_wrapper
    def get_driver(cursor, driver_phone: str) -> Driver or None:
        cursor.execute(f"""SELECT * FROM drivers WHERE driver_phone like '{driver_phone}'""")
        res = cursor.fetchall()
        if not res:
            return None
        return Driver(*res[0])

    @staticmethod
    @postgres_wrapper
    def get_schedule(cursor, start: dt.datetime = None, end: dt.datetime = None):
        query = f"""SELECT * FROM drivers_schedule"""
        if start and end:
            query += f""" WHERE dtstart <= {start} AND {end} <= dtend"""
        cursor.execute(query)
        return [DriverSchedule(*s) for s in cursor.fetchall()]

    @staticmethod
    @postgres_wrapper
    def get_driver_schedule(cursor, driver_phone):
        cursor.execute(f"""SELECT * FROM drivers_schedule WHERE driver_phone like '{driver_phone}'""")
        return [DriverSchedule(*s) for s in cursor.fetchall()]
