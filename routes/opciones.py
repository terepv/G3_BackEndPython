from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from db.models import Opcion
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum
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
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista de todas las opciones.

    Requiere estar autenticado con rol de ADMIN, FISCALIZADOR u Organismo Sectorial para acceder a este recurso.
    """
    opciones = db.query(Opcion).all()
    return opciones


@router.post(
    "/", 
    summary="Añade una opcion", 
    status_code=201
)
def add_opcion(
    db: SyncDbSessionDep,
    opcion: OpcionCreate = Body(
        openapi_examples={
            "default": get_example("opcion_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega una opción.

    Argumentos:
    - nombre de la opción (str)

    Devuelve mensaje de confirmación con el recurso creado.
    
    Requiere estar autenticado con rol de ADMIN para acceder a este recurso.
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


@router.put(
    "/{id_opcion}",
    summary="Actualiza una opción por su id",
    status_code=201,
)

def update_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
    opcion_update: OpcionCreate = Body(
        openapi_examples={
            "default": get_example("opcion_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza el texto de una opción existente.

    Solo los usuarios con rol ADMIN pueden actualizar una opción.
    """
    db_opcion = db.get(Opcion, id_opcion)

    if not db_opcion:
        raise HTTPException(status_code=404, detail="Opción no encontrada")

    nombre_opcion = opcion_update.opcion
    if db.query(Opcion).filter(Opcion.opcion.ilike(nombre_opcion), Opcion.id_opcion != id_opcion).first():
        raise HTTPException(status_code=409, detail="Ya existe una opción con ese nombre")
    if len(opcion_update.opcion) == 0:
        raise HTTPException(status_code=400, detail="Opción no puede estar vacío")
    if len(opcion_update.opcion) > 100:
        raise HTTPException(status_code=400, detail="Opción muy larga")

    db_opcion.opcion = nombre_opcion
    db.commit()
    db.refresh(db_opcion)

    return db_opcion





@router.delete(
    "/{id_opcion}",
    summary="Elimina una opción",
)
def delete_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una opción por su id.

    Requiere ser usuario de ADMIN para acceder a este recurso.
    """
    opcion = db.query(Opcion).filter(Opcion.id_opcion == id_opcion).first()
    if opcion:
        db.delete(opcion)
        db.commit()
    return {"message": "Se eliminó opción"}
