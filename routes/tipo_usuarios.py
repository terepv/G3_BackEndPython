from fastapi import APIRouter, Depends
from db.models import TipoUsuario
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import UsuarioOut

router = APIRouter(prefix="/tipo_usuarios", tags=["Tipos de Usuarios"])


@router.get(
    "/",
    response_model=list[TipoUsuario],
    summary="Obtener todos los tipos de usuarios",
)
def read_tipo_datos(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todos los tipos de usuarios.

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    tipo_datos = db.query(TipoUsuario).all()
    return tipo_datos
