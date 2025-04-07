from fastapi import APIRouter, Depends
from db.models import RolResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get(
    "/",
    response_model=list[RolResponse],
    response_model_exclude_none=True,
    summary="Obtener todos los roles de usuario",
)
async def read_roles(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista de todos los roles de usuario.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    roles = db.query(RolResponse).filter(RolResponse.eliminado_por == None).all()
    return roles