from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from app.db.models import ComunaResponse, RegionResponse
from app.shared.enums import RolesEnum
from app.shared.schemas import ComunaCreate, ComunaOut, UsuarioOut
from app.shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from app.shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/comunas", tags=["Comunas"])


@router.get(
    "/",
    response_model=list[ComunaOut],
    response_model_exclude_none=True,
    summary="Obtener todas las comunas",
)
def read_comunas(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las comunas.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    comunas = db.query(ComunaResponse).filter(ComunaResponse.eliminado_por == None).join(RegionResponse).all()
    return comunas


@router.get(
    "/comuna/{id_comuna}",
    response_model=ComunaOut,
    response_model_exclude_none=True,
    summary="Obtener una comuna por su id",
)
def read_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una comuna por su id.

    Argumentos:
    - id comuna (int)

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    comuna = db.query(ComunaResponse).filter(ComunaResponse.id_comuna == id_comuna, ComunaResponse.eliminado_por == None).first()
    if not comuna:
        raise HTTPException(status_code=404, detail="No existe comuna con ese id")
    return comuna

@router.post(
    "/", 
    summary="Añade una comuna", 
    status_code=201,
    response_model_exclude_none=True,
)
def add_comuna(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    comuna: ComunaCreate = Body(
        openapi_examples={
            "default": get_example("comuna_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega una comuna.
    
    Argumentos:
    - nombre de la comuna (str)
    - id_region (int)

    Devuelve un mensaje de confirmación con el recurso creado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    if db.query(ComunaResponse).filter(ComunaResponse.comuna.ilike(comuna.comuna), ComunaResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Comuna ya existe")
    
    if not db.query(RegionResponse).filter(RegionResponse.id_region == comuna.id_region, RegionResponse.eliminado_por == None).first():
        raise HTTPException(status_code=404, detail="No existe región con ese id")

    data = ComunaResponse(
        comuna=comuna.comuna,
        id_region=comuna.id_region,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return {"message": "Se creó comuna", "comuna": data}

@router.put(
    "/{comuna_id}", 
    summary="Actualiza una comuna por su id", 
    response_model_exclude_none=True,
)
def update_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    comuna: ComunaCreate = Body(
        openapi_examples={
            "default": get_example("comuna_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza una comuna por su id.
    
    Argumentos
    - id de la comuna (int)
    - nombre de la comuna (str)
    - id_region (int)

    Devuelve un mensaje de confirmación con el recurso creado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """

    data = db.query(ComunaResponse).filter(ComunaResponse.id_comuna == id_comuna, ComunaResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe comuna con ese id")
    if db.query(ComunaResponse).filter(ComunaResponse.id_comuna != id_comuna, ComunaResponse.comuna.ilike(comuna.comuna), ComunaResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Comuna ya existe")
    if not db.query(RegionResponse).filter(RegionResponse.id_region == comuna.id_region, RegionResponse.eliminado_por == None).first():
        raise HTTPException(status_code=404, detail="No existe región con ese id")
    data.fecha_actualizacion = get_local_now_datetime()
    data.comuna = comuna.comuna
    data.id_region = comuna.id_region
    data.actualizado_por = user.email
    db.commit()
    return (
        {"message": "Se actualizó comuna", "comuna": data}
    )

@router.delete(
    "/{id_comuna}",
    summary="Elimina una comuna por su id",
)
def delete_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una comuna por su id.

    Argumentos:
    - id comuna (int)

    Devuelve mensaje de confirmación.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    comuna = db.query(ComunaResponse).filter(ComunaResponse.id_comuna == id_comuna, ComunaResponse.eliminado_por == None).first()
    if comuna:
        comuna.fecha_eliminacion = get_local_now_datetime()
        comuna.eliminado_por = user.email
        db.commit()

    return {"message": "Se eliminó comuna"}