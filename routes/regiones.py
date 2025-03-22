from fastapi import APIRouter, Depends, HTTPException
from db.models import Region
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum

router = APIRouter(prefix="/regiones", tags=["Regiones"])


@router.get(
    "/",
    response_model=list[Region],
    summary="Obtener todas las regiones",
)
def read_regions(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista de todas las regiones.

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    regions = db.query(Region).all()
    return regions


@router.get(
    "/{id_region}",
    response_model=Region,
    summary="Obtener una region por su id",
)
def read_region(
    id_region: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una región por su id.

    Argumentos:
    - id región (int)

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    region = db.query(Region).filter(Region.id_region == id_region).first()
    if not region:
        raise HTTPException(status_code=404, detail="No existe región con ese id")
    return region
