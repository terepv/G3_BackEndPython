from fastapi import APIRouter, Depends, HTTPException
from db.models import ComunaResponse, Region
from shared.enums import RolesEnum
from shared.schemas import ComunaOut
from shared.dependencies import RoleChecker, SyncDbSessionDep

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
    comunas = db.query(ComunaResponse).filter(ComunaResponse.eliminado_por == None).join(Region).all()
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
