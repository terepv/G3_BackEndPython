from fastapi import APIRouter, Body, HTTPException
from db.models import Opcion
from shared.dependencies import SyncDbSessionDep
from shared.schemas import OpcionCreate
from shared.utils import get_example

router = APIRouter(prefix="/opciones", tags=["Opciones"])


@router.get(
    "/",
    response_model=list[Opcion],
    summary="Obtener todas las opciones",
)
def read_opciones(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las opciones. """
    opciones = db.query(Opcion).all()
    return opciones


@router.post(
    "/", summary="Añade una opcion", status_code=201
)
def add_opcion(
    db: SyncDbSessionDep,
    opcion: OpcionCreate = Body(
        openapi_examples={
            "default": get_example("opcion_post"),
        }
    ),
):
    """
    Agrega una opción a la base de datos.
    Argumentos:
    - opción (str)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    nombre_opcion = opcion.opcion
    if db.query(Opcion).filter(Opcion.opcion.ilike(nombre_opcion)).first():
        raise HTTPException(status_code=409, detail="Opcion ya existe")
    if len(opcion.opcion) == 0:
        raise HTTPException(status_code=400, detail="Opcion no puede ser vacío")
    if len(opcion.opcion) > 100:
        raise HTTPException(status_code=400, detail="Opcion muy larga")

    opcion = Opcion(opcion=nombre_opcion)
    db.add(opcion)
    db.commit()
    db.refresh(opcion)
    return {"message": "Se creó opcion", "opcion": opcion}


@router.delete(
    "/{id_opcion}",
    summary="Elimina una opción",
)
def delete_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
):
    """
    Elimina una opción por su id.
    Argumentos:
    - id opción (int)
    
    Devuelve mensaje de confirmación.
    """
    opcion = db.query(Opcion).filter(Opcion.id_opcion == id_opcion).first()
    if opcion:
        db.delete(opcion)
        db.commit()
    return {"message": "Se eliminó opción"}
