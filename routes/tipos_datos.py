from fastapi import APIRouter
from db.models import TipoDato
from shared.dependencies import SyncDbSessionDep

router = APIRouter(prefix="/tipos_datos", tags=["Tipos de Datos"])

@router.get("/", response_model=list[TipoDato], summary="Obtener todos los tipos de datos")
def read_tipo_datos(
    db: SyncDbSessionDep,
):
    tipo_datos = db.query(TipoDato).all()
    return tipo_datos