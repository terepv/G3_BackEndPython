from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from db.models import OpcionResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import OpcionCreate, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/opciones", tags=["Opciones"])


@router.get(
    "/",
    response_model=list[OpcionResponse],
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
    opciones = db.query(OpcionResponse).filter(OpcionResponse.eliminado_por == None).all()
    return opciones


@router.post(
    "/", 
    summary="Añade una opcion", 
    status_code=201,
    response_model_exclude_none=True,
)
def add_opcion(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
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
    if db.query(OpcionResponse).filter(OpcionResponse.opcion.ilike(nombre_opcion), OpcionResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Opcion ya existe")
    if len(opcion.opcion) == 0:
        raise HTTPException(status_code=400, detail="Opcion no puede ser vacío")
    if len(opcion.opcion) > 100:
        raise HTTPException(status_code=400, detail="Opcion muy larga")

    data = OpcionResponse(
        opcion=nombre_opcion,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message": "Se creó opcion", "opcion": data}


@router.put(
    "/{id_opcion}",
    summary="Actualiza una opción por su id",
    response_model_exclude_none=True,
)

def update_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
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
    db_opcion = db.get(OpcionResponse, id_opcion)

    if not db_opcion:
        raise HTTPException(status_code=404, detail="Opción no encontrada")

    nombre_opcion = opcion_update.opcion
    if db.query(OpcionResponse).filter(OpcionResponse.opcion.ilike(nombre_opcion), OpcionResponse.id_opcion != id_opcion, OpcionResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Ya existe una opción con ese nombre")
    if len(opcion_update.opcion) == 0:
        raise HTTPException(status_code=400, detail="Opción no puede estar vacío")
    if len(opcion_update.opcion) > 100:
        raise HTTPException(status_code=400, detail="Opción muy larga")

    db_opcion.opcion = nombre_opcion
    db_opcion.fecha_modificacion = get_local_now_datetime()
    db_opcion.modificado_por = user.email
    db.commit()
    db.refresh(db_opcion)

    return {"message": "Se actualizó opción", "opcion": db_opcion}


@router.delete(
    "/{id_opcion}",
    summary="Elimina una opción",
)
def delete_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una opción por su id.

    Requiere ser usuario de ADMIN para acceder a este recurso.
    """
    opcion = db.query(OpcionResponse).filter(OpcionResponse.id_opcion == id_opcion, OpcionResponse.eliminado_por == None).first()
    if opcion:
        opcion.fecha_eliminacion = get_local_now_datetime()
        opcion.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó opción"}
