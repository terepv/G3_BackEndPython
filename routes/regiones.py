from fastapi import APIRouter, Depends, HTTPException
from db.models import RegionResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum

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
