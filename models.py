# PPDA models
from pydantic import BaseModel


class ComunaModel(BaseModel):
    id_comuna: int
    nombre_comuna: str
    id_region: int

