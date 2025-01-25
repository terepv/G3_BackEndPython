from domain import Comuna
import psycopg2
from postgres_connection import *

def get_all_comuna():
    res = db_select("SELECT * FROM comuna")
    if res:
        return res
    else:
        return None