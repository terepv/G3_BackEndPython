from fastapi import APIRouter, HTTPException
from db.models import Comuna, Region
from shared.schemas import ComunaOut
from shared.dependencies import SyncDbSessionDep

router = APIRouter(prefix="/comunas", tags=["Comunas"])

@router.get("/", response_model=list[ComunaOut], summary="Obtener todas las comunas")
def read_comunas(
    db: SyncDbSessionDep,
):
    comunas = db.query(Comuna).join(Region).all()
    return comunas

@router.get("/comuna/{id_comuna}", response_model=ComunaOut, summary="Obtener una comuna por su id")
def read_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
):
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()
    if not comuna:
        raise HTTPException(status_code=404, detail="No existe comuna con ese id")
    return comuna