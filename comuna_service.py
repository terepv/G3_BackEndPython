from domain import Comuna
import pandas as pd
from postgres_connection import *

def get_all_comuna():
    res = db_select("SELECT * FROM comuna")
    if res:
        return res
    else:
        return None