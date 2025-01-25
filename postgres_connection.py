import psycopg2
from dotenv import load_dotenv
from os import environ as env
from datetime import datetime

load_dotenv()

class DBConection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=env["POSTGRES_DBNAME"],
            user=env["POSTGRES_USER"],
            password=env["POSTGRES_PASSWORD"],
            host=env["POSTGRES_HOST"],
            port=env["POSTGRES_PORT"],
        )

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


def db_execute(query: str, values: tuple):
    with DBConection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, values)
            connection.commit()
        except Exception as e:
            connection.rollback()
        finally:
            cursor.close()


def db_select(query: str):
    with DBConection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()