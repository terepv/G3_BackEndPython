from fastapi import APIRouter, Depends
from db.models import TipoDato
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum

router = APIRouter(prefix="/tipos_datos", tags=["Tipos de Datos"])


@router.get(
    "/",
    response_model=list[TipoDato],
    summary="Obtener todos los tipos de datos",
)
def read_tipo_datos(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todos los tipos de datos.

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    tipo_datos = db.query(TipoDato).all()
    return tipo_datos
