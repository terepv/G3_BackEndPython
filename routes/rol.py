from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from db.models import Rol
from shared.dependencies import AsyncDbSessionDep, RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.schemas import Rol
from shared.enums import RolesEnum

router = APIRouter(prefix="/rol", tag=["rol"])


@router.get(
    "/",
    response_model=list[Rol],
    summary="Obtener todos los roles de usuario",
)
async def read_roles(
    db: AsyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Devuelve una lista de todos los roles de usuario.

    Requiere permisos de ADMINISTRADOR para acceder a este recurso.
    """
    result = await db.execute(select(Rol))
    roles = result.scalars().all()
    return roles