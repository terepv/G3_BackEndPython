from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Frecuencia, FrecuenciaResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import FrecuenciaCreate, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/frecuencias", tags=["Frecuencias"])


@router.get(
    "/",
    response_model=list[FrecuenciaResponse],
    summary="Obtener todas las frecuencias",
)
def read_frecuencias(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las frecuencias.
    
    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    frecuencias = db.query(FrecuenciaResponse).filter(FrecuenciaResponse.eliminado_por == None).all()
    return frecuencias


@router.get(
    "/{id_frecuencia}",
    response_model=FrecuenciaResponse,
    response_model_exclude_none=True,
    summary="Obtener una frecuencia por su id",
)
def read_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una frecuencia por su id.

    Argumentos:
    - id de frecuencia (int)

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """ 
    frecuencia = (
        db.query(FrecuenciaResponse).filter(FrecuenciaResponse.id_frecuencia == id_frecuencia, FrecuenciaResponse.eliminado_por == None).first()
    )
    if not frecuencia:
        raise HTTPException(status_code=404, detail="No existe frecuencia con ese id")
    return frecuencia


@router.post(
    "/",
    summary="Añade una frecuencia",
    status_code=201,
    response_model_exclude_none=True,
)
def add_frecuencia(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    frecuencia: FrecuenciaCreate = Body(
        openapi_examples={
            "default": get_example("frecuencia_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega una frecuencia a la base de datos.

    Argumentos:
    - frecuencia (str)

    Devuelve mensaje de confirmación con el recurso creado.
    
    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    nombre_frecuencia = frecuencia.frecuencia
    if (
        db.query(FrecuenciaResponse)
        .filter(FrecuenciaResponse.frecuencia.ilike(nombre_frecuencia))
        .first()
    ):
        raise HTTPException(status_code=409, detail="Frecuencia ya existe")
    if len(nombre_frecuencia) < 3:
        raise HTTPException(status_code=400, detail="Nombre de frecuencia muy corto")
    if len(nombre_frecuencia) > 100:
        raise HTTPException(status_code=400, detail="Nombre de frecuencia muy largo")

    frecuencia = FrecuenciaResponse(
        frecuencia=nombre_frecuencia,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
        )
    db.add(frecuencia)
    db.commit()
    db.refresh(frecuencia)
    return {"message": "Se creó frecuencia", "frecuencia": frecuencia}

@router.put(
        "/{id_frecuencia}",
        summary="Actualiza una frecuencia por su id",
        status_code=201,
        response_model_exclude_none=True
)
def update_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    frecuencia: FrecuenciaCreate = Body(
        openapi_examples={
            "default": get_example("frecuencia_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza una frecuencia por su id.
    
    Argumentos:
    - id de la frecuencia (int)
    - nombre de la frecuencia (str)

    Devuelve un mensaje de confirmación con el recurso actualizado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    data = db.query(FrecuenciaResponse).filter(FrecuenciaResponse.id_frecuencia == id_frecuencia, FrecuenciaResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe frecuencia con ese id")

    if (db.query(FrecuenciaResponse)
        .filter(FrecuenciaResponse.frecuencia.ilike(frecuencia.frecuencia), 
                FrecuenciaResponse.id_frecuencia != id_frecuencia).first()):
        raise HTTPException(status_code=409, detail="Frecuencia ya existe")

    data.frecuencia = frecuencia.frecuencia
    data.fecha_actualizacion = get_local_now_datetime()
    data.actualizado_por = user.email
    db.commit()

    return {"message": "Se actualizó frecuencia", "frecuencia": frecuencia}

@router.delete(
    "/{id_frecuencia}",
    summary="Elimina una frecuencia por su id",
    status_code=204,
)
def delete_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una frecuencia por su id.

    Argumentos:
    - id de frecuencia (int)

    Devuelve mensaje de confirmación.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    frecuencia = db.query(FrecuenciaResponse).filter(FrecuenciaResponse.id_frecuencia == id_frecuencia, FrecuenciaResponse.eliminado_por == None).first()
    if frecuencia:
        frecuencia.fecha_eliminacion = get_local_now_datetime()
        frecuencia.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó frecuencia"}
