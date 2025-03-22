from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Frecuencia
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum
from shared.schemas import FrecuenciaCreate
from shared.utils import get_example

router = APIRouter(prefix="/frecuencias", tags=["Frecuencias"])


@router.get(
    "/",
    response_model=list[Frecuencia],
    summary="Obtener todas las frecuencias",
)
def read_frecuencias(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las frecuencias.
    
    Requiere estar autenticado con rol de SMA u Organismo Sectorial para acceder a este recurso.
    """
    frecuencias = db.query(Frecuencia).all()
    return frecuencias


@router.get(
    "/{id_frecuencia}",
    response_model=Frecuencia,
    summary="Obtener una frecuencia por su id",
)
def read_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una frecuencia por su id.

    Requiere estar autenticado con rol de SMA u Organismo Sectorial para acceder a este recurso.
    """ 
    frecuencia = (
        db.query(Frecuencia).filter(Frecuencia.id_frecuencia == id_frecuencia).first()
    )
    if not frecuencia:
        raise HTTPException(status_code=404, detail="No existe frecuencia con ese id")
    return frecuencia


@router.post(
    "/",
    summary="Añade una frecuencia",
    status_code=201,
)
def add_frecuencia(
    db: SyncDbSessionDep,
    frecuencia: FrecuenciaCreate = Body(
        openapi_examples={
            "default": get_example("frecuencia_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Agrega una frecuencia a la base de datos.

    Argumentos:
    - Frecuencia (str)

    Devuelve mensaje de confirmación con el recurso creado.
    
    Requiere permisos de SMA para acceder a este recurso.
    """
    nombre_frecuencia = frecuencia.frecuencia
    if (
        db.query(Frecuencia)
        .filter(Frecuencia.frecuencia.ilike(nombre_frecuencia))
        .first()
    ):
        raise HTTPException(status_code=409, detail="Frecuencia ya existe")
    if len(nombre_frecuencia) < 3:
        raise HTTPException(status_code=400, detail="Nombre de frecuencia muy corto")
    if len(nombre_frecuencia) > 100:
        raise HTTPException(status_code=400, detail="Nombre de frecuencia muy largo")

    frecuencia = Frecuencia(frecuencia=nombre_frecuencia)
    db.add(frecuencia)
    db.commit()
    db.refresh(frecuencia)
    return {"message": "Se creó frecuencia", "frecuencia": frecuencia}


@router.delete(
    "/{id_frecuencia}",
    summary="Elimina una frecuencia",
)
def delete_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Elimina una frecuencia por su id.

    Argumentos:
    - id_frecuencia: El id de la frecuencia a eliminar.

    Devuelve mensaje de confirmación con el recurso eliminado.

    Requiere permisos de SMA para acceder a este recurso.
    """
    frecuencia = (
        db.query(Frecuencia).filter(Frecuencia.id_frecuencia == id_frecuencia).first()
    )
    if frecuencia:
        db.delete(frecuencia)
        db.commit()
    return {"message": "Se eliminó frecuencia"}
