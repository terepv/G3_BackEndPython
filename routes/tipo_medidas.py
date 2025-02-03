from fastapi import APIRouter, Body, HTTPException
from db.models import TipoMedida
from shared.dependencies import SyncDbSessionDep
from shared.schemas import TipoMedidaCreate
from shared.utils import get_example

router = APIRouter(prefix="/tipo_medidas", tags=["Tipo Medidas"])

@router.get("/", response_model=list[TipoMedida], summary="Obtener todos los tipos de medidas")
def read_tipo_medidas(
    db: SyncDbSessionDep,
):
    tipo_medidas = db.query(TipoMedida).all()
    return tipo_medidas

@router.get("/{id_tipo_medida}", response_model=TipoMedida, summary="Obtener un tipo de medida por su id")
def read_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
):
    tipo_medida = db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==id_tipo_medida).first()
    if not tipo_medida:
        raise HTTPException(status_code=404, detail="No existe tipo de medida con ese id")
    return tipo_medida

@router.post("/", summary="Añade un tipo de medida", status_code=201)
def add_tipo_medida(
    db: SyncDbSessionDep,
    tipo_medida: TipoMedidaCreate = Body(
        openapi_examples={
            "default": get_example("tipo_medida_post"),
        }
    ),
):
    nombre_tipo_medida = tipo_medida.tipo_medida
    
    if db.query(TipoMedida).filter(TipoMedida.tipo_medida.ilike(nombre_tipo_medida)).first():
        raise HTTPException(status_code=409, detail="Tipo de medida ya existe")
    if len(nombre_tipo_medida) < 3:
        raise HTTPException(status_code=400, detail="Nombre de tipo de medida muy corto")
    if len(nombre_tipo_medida) > 100:
        raise HTTPException(status_code=400, detail="Nombre de tipo de medida muy largo")
    
    tipo_medida = TipoMedida(tipo_medida=nombre_tipo_medida)
    db.add(tipo_medida)
    db.commit()
    db.refresh(tipo_medida)
    return {"message": "Se creó tipo de medida", "tipo de medida": tipo_medida}

@router.delete("/{id_tipo_medida}", summary="Elimina un tipo de medida")
def delete_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
):
    tipo_medida = db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==id_tipo_medida).first()
    if tipo_medida:
        db.delete(tipo_medida)
        db.commit()
    return {"message": "Se eliminó tipo de medida"}