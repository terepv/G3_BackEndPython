from fastapi import APIRouter, Depends
from db.models import TipoUsuario
from shared.dependencies import SyncDbSessionDep, get_user_from_token_data
from shared.schemas import UsuarioOut

router = APIRouter(prefix="/tipo_usuarios", tags=["Tipos de Usuarios"])


@router.get(
    "/",
    response_model=list[TipoUsuario],
    summary="Obtener todos los tipos de usuarios",
)
def read_tipo_datos(
    db: SyncDbSessionDep,
    _: UsuarioOut | None = Depends(get_user_from_token_data),
):
    """ Devuelve una lista de todos los tipos de usuarios. 
    
    Requiere estar autenticado para acceder a este recurso.
    """
    tipo_datos = db.query(TipoUsuario).all()
    return tipo_datos
