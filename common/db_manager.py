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
    def insert(cursor, order: Order) -> Order:
        cursor.execute(f"""INSERT INTO orders
         VALUES (DEFAULT,
                 {order.user.id},
                 {order.driver.id},
                 '{order.transport.type}',
                 '{order.start}',
                 '{order.end}',
                 {order.latitude},
                 {order.longitude},
                 '{order.status}')
         RETURNING id""")
        order_id = cursor.fetchall()[0][0]
        return PG_Orders.get(order_id)

    @staticmethod
    @postgres_wrapper
    def get(cursor, order_id: int) -> Order:
        cursor.execute(f"""SELECT * FROM orders WHERE id = {order_id}""")
        order = Order(*cursor.fetchall()[0])
        return order

    @staticmethod
    @postgres_wrapper
    def create_table(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
        id serial PRIMARY KEY,
        user_id int,
        driver_id int,
        transport_type varchar(100),
        dtstart timestamp,
        dtend timestamp,
        latitude float,
        longitude float,
        status varchar(100)
        )""")
