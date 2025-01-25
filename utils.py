import pytz
from datetime import datetime


from config import APP_TIMEZONE_LOCAL


def get_local_now_datetime() -> datetime:
    local_tz = pytz.timezone(APP_TIMEZONE_LOCAL)
    return datetime.now(local_tz)