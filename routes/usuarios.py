from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models import TipoUsuario, Usuario
from shared.dependencies import AsyncDbSessionDep, SyncDbSessionDep, get_user_from_db
from shared.schemas import UsuarioCreate, UsuarioOut
from shared.utils import get_example

router = APIRouter(prefix="/usuarios", tags=["Usuarios"],
                   dependencies=[Depends(get_user_from_db)])


@router.get(
    "/",
    response_model=list[UsuarioOut],
    summary="Obtener todos los usuarios",
    description="Devuelve un listado de todos los usuarios",
)
async def read_users(
    db: AsyncDbSessionDep,
):
    result = await db.scalars(select(Usuario).options(selectinload(Usuario.tipo_usuario)))
    users = result.all()
    return users


@router.get(
    "/{id_usuario}",
    response_model=UsuarioOut,
    summary="Obtener un usuario por su id",
    description="Devuelve un usuario por su id",
)
def read_user(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    usuario = db.query(Usuario).filter(Usuario.id_tipo_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe usuario con ese id")
    return usuario


@router.post(
    "/", summary="Añade un usuario", status_code=201, description="Crea un usuario"
)
def add_organismo(
    db: SyncDbSessionDep,
    usuario: UsuarioCreate = Body(
        openapi_examples={
            "default": get_example("usuario_post"),
        }
    ),
):
    if db.query(Usuario).filter(Usuario.email.ilike(usuario.email)).first():
        raise HTTPException(status_code=409, detail="Usuario ya existe")
    if (
        not db.query(TipoUsuario)
        .filter(TipoUsuario.id_tipo_usuario == usuario.id_tipo_usuario)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de usuario no existe")

    data = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        activo=usuario.activo,
        id_tipo_usuario=usuario.id_tipo_usuario,
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message": "Se creó el usuario", "usuario": data}


@router.delete(
    "/{id_usuario}",
    summary="Elimina un usuario por su id",
    description="Elimina un usuario por su id",
)
def delete_usuario(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if usuario:
        db.delete(usuario)
        db.commit()

    return {"message": "Se eliminó usuario"}
