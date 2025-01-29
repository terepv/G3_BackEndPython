import json
import pathlib
from datetime import datetime
from fastapi.openapi.models import Example

def get_example(filename: str) -> Example:
    api_examples_path = pathlib.Path(__file__).parent / "examples"
    filepath = api_examples_path / f"{filename}.json"
    if not filepath.exists():
        raise FileNotFoundError(f"Example file not found: {filepath}")
    with open(filepath) as f:
        return Example(value=json.load(f))
    
example_data = {}