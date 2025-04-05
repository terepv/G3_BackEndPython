from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Region, RegionResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import RegionCreate, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/regiones", tags=["Regiones"])


@router.get(
    "/",
    response_model=list[RegionResponse],
    response_model_exclude_none=True,
    summary="Obtener todas las regiones",
)
def read_regions(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista de todas las regiones.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    regions = db.query(RegionResponse).filter(RegionResponse.eliminado_por == None).all()
    return regions


@router.get(
    "/{id_region}",
    response_model=RegionResponse,
    response_model_exclude_none=True,
    summary="Obtener una region por su id",
)
def read_region(
    id_region: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una región por su id.

    Argumentos:
    - id región (int)

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    region = db.query(RegionResponse).filter(RegionResponse.id_region == id_region, RegionResponse.eliminado_por == None).first()
    if not region:
        raise HTTPException(status_code=404, detail="No existe región con ese id")
    return region


@router.post(
    "/",
    response_model=RegionResponse,
    status_code=201, 
    response_model_exclude_none=True,
    summary="Crear una nueva región",
)
def add_region(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    region: RegionCreate = Body(
        openapi_examples={
            "default": get_example("region_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):


    """
    Crea una nueva región.

    Argumentos:
    - nombre del plan (str)

    Devuelve un mensaje de confirmación con el recurso actualizado.
    Requiere rol de Administrador.
    """

    if db.query(Region).filter(Region.nombre.ilike(region.nombre)).first():
        raise HTTPException(status_code=409, detail="Región ya existe")

    data = RegionResponse(
        region=region.nombre,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return {"message": "Se creó una región", "región": data}