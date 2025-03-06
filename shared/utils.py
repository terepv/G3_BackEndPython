import json
import pathlib
import pytz
from datetime import datetime, timedelta, timezone
from fastapi.openapi.models import Example
from jose import jwt

from config import ACCESS_TOKEN_EXPIRE_MINUTES, APP_TIMEZONE_LOCAL, TOKEN_ALGORITHM, TOKEN_SECRET_KEY


def get_local_now_datetime() -> datetime:
    local_tz = pytz.timezone(APP_TIMEZONE_LOCAL)
    return datetime.now(local_tz)

def get_example(filename: str) -> Example:
    api_examples_path = pathlib.Path(__file__).parent.parent / "examples"
    filepath = api_examples_path / f"{filename}.json"
    if not filepath.exists():
        raise FileNotFoundError(f"Example file not found: {filepath}")
    with open(filepath) as f:
        return Example(value=json.load(f))
    
example_data = {}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)