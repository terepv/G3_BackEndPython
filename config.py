from dotenv import load_dotenv
from os import environ as env

try:
    load_dotenv()
except ImportError:
    pass

APP_TIMEZONE_LOCAL = env["APP_TIMEZONE_LOCAL"]
DB_NAME = env["DB_DBNAME"]
DB_USER = env["DB_USER"]
DB_PASSWORD = env["DB_PASSWORD"]
DB_HOST = env["DB_HOST"]
DB_PORT = env["DB_PORT"]