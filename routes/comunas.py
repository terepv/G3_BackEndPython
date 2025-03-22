from fastapi import APIRouter, Depends, HTTPException
from db.models import Comuna, Region
from shared.enums import RolesEnum
from shared.schemas import ComunaOut
from shared.dependencies import RoleChecker, SyncDbSessionDep

router = APIRouter(prefix="/comunas", tags=["Comunas"])


@router.get(
    "/",
    response_model=list[ComunaOut],
    summary="Obtener todas las comunas",
)
def read_comunas(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las comunas.

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    comunas = db.query(Comuna).join(Region).all()
    return comunas


@router.get(
    "/comuna/{id_comuna}",
    response_model=ComunaOut,
    summary="Obtener una comuna por su id",
)
def read_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una comuna por su id.

    Argumentos:
    - id comuna (int)

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()
    if not comuna:
        raise HTTPException(status_code=404, detail="No existe comuna con ese id")
    return comuna
