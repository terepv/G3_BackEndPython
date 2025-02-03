import json
import pathlib
import pytz
from datetime import datetime
from fastapi.openapi.models import Example

from config import APP_TIMEZONE_LOCAL


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