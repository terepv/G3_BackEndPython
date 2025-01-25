from fastapi import FastAPI
import comuna_service
from models import ComunaModel

app = FastAPI()

@app.get("/")
def get_all_comunas():
    res = comuna_service.get_all_comuna()
    return res