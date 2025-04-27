from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from app.db.models import Usuario, UsuarioResponse
from app.shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from app.shared.schemas import UsuarioCreate, UsuarioOut
from app.shared.utils import get_example, get_password_hash, get_local_now_datetime
from app.shared.enums import RolesEnum

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    response_model_exclude_none=True,
    summary="Obtener todos los usuarios",
)
def read_users(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Devuelve una lista de todos los usuarios.

    Requiere permisos de administrador para acceder a este recurso.
    """
    usuarios = db.query(UsuarioResponse).filter(UsuarioResponse.eliminado_por == None).all()
    # Asegúrate de que 'password' esté excluido manualmente si no está siendo excluido por el response_model_exclude
    for usuario in usuarios:
        del usuario.password  # Elimina manualmente la columna 'password' de cada usuario

    return usuarios


@router.get(
    "/{id_usuario}",
    response_model=UsuarioOut,
    summary="Obtener un usuario por su id",
)
def read_user(
    id_usuario: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Devuelve un usuario por su id.
    
    Argumentos:
    - id usuario (int)

    Requiere permisos de administrador para acceder a este recurso.
    """
    usuario = db.query(UsuarioResponse).filter(UsuarioResponse.id_usuario == id_usuario, UsuarioResponse.eliminado_por == None).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe usuario con ese id")
    return usuario


@router.post(
    "/", summary="Añade un usuario", status_code=201
)
def add_usuario(
    db: SyncDbSessionDep,
    user_create: Annotated[UsuarioOut, Depends(get_user_from_token_data)], #Usuario que esta logeado
    usuario: UsuarioCreate = Body(
        openapi_examples={
            "default": get_example("usuario_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega un usuario a la base de datos.

    Argumentos:
    - email del usuario (str)
    - nombre del usuario (str)
    - apellido del usuario (str)
    - id del tipo de usuario (int)
    - password del usuario (str)
    - activo (bool)

    Devuelve mensaje de confirmación con el recurso creado.

    Requiere permisos de administrador para acceder a este recurso.
    """
    if db.query(UsuarioResponse).filter(UsuarioResponse.email.ilike(usuario.email), UsuarioResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Usuario ya existe")
    
    data = UsuarioResponse(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        activo=usuario.activo,
        id_rol=usuario.id_rol,
        id_organismo_sectorial=usuario.id_organismo_sectorial,
        password=get_password_hash(usuario.password),
        fecha_creacion=get_local_now_datetime(),
        creado_por=user_create.email
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message": "Se creó el usuario", "usuario": data}

@router.put(
    "/{id_usuario}",
    summary="Actualiza un usuario por su id",
    response_model_exclude_none=True,
)
def update_user(
    id_usuario: int,
    db: SyncDbSessionDep,
    user_create: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    usuario: UsuarioCreate = Body(
        openapi_examples={
            "default": get_example("usuario_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza un usuario por su id.

    Argumentos:
    - nombre de la persona (str)
    - apellido de la persona (str)
    - email de la persona (str)

    Devuelve mensaje de confirmación con el recurso actualizado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """

    data = db.query(UsuarioResponse).filter(UsuarioResponse.id_usuario == id_usuario, UsuarioResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe usuario con ese id")
    if db.query(UsuarioResponse).filter(UsuarioResponse.id_usuario != id_usuario, UsuarioResponse.email.ilike(usuario.email), UsuarioResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Email ya existe")
    data.nombre=usuario.nombre
    data.apellido=usuario.apellido
    data.email=usuario.email
    data.activo=usuario.activo
    data.id_rol=usuario.id_rol
    data.id_organismo_sectorial=usuario.id_organismo_sectorial
    data.fecha_actualizacion = get_local_now_datetime()
    data.actualizado_por = user_create.email
    db.commit()
    return (
        {"message": "Se actualizó usuario", "usuario": data}
    )


@router.delete(
    "/{id_usuario}",
    summary="Elimina un usuario por su id",
)
def delete_usuario(
    id_usuario: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina un usuario por su id.

    Argumentos:
    - id del usuario (int)

    Devuelve mensaje de confirmación con el recurso eliminado.

    Requiere permisos de administrador para acceder a este recurso.
    """
    usuario= db.query(UsuarioResponse).filter(UsuarioResponse.id_usuario == id_usuario, UsuarioResponse.eliminado_por == None).first()
    if usuario:
        usuario.fecha_eliminacion = get_local_now_datetime()
        usuario.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó usuario"}