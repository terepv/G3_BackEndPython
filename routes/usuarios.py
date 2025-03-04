from fastapi import APIRouter, Body, HTTPException
from db.models import TipoUsuario, Usuario
from shared.dependencies import SyncDbSessionDep
from shared.schemas import UsuarioCreate, UsuarioOut
from shared.utils import get_example

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get(
    "/",
    response_model=list[UsuarioOut],
    summary="Obtener todos los usuarios",
)
def read_users(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todos los usuarios. """
    users = db.query(Usuario).all()
    return users


@router.get(
    "/{id_usuario}",
    response_model=Usuario,
    summary="Obtener un usuario por su id",
)
def read_user(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    """ 
    Devuelve un usuario por su id.
    Argumentos: 
    - id usuario (int)
    """
    usuario = db.query(Usuario).filter(Usuario.id_tipo_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe usuario con ese id")
    return usuario


@router.post(
    "/", summary="Añade un usuario", status_code=201
)
def add_organismo(
    db: SyncDbSessionDep,
    usuario: UsuarioCreate = Body(
        openapi_examples={
            "default": get_example("usuario_post"),
        }
    ),
):
    """
    Agrega un usuario.
    Argumentos:
    - nombre (str)
    - apellido (str)
    - email (str)
    - usuario activo (bool)
    - id tipo de usuario (int)

    Devuelve mensaje de confirmación con el recurso creado.
    """
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
)
def delete_usuario(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    """
    Elimina un usuario por su id.
    Argumentos: 
    - id usuario (int)

    Devuelve mensaje de confirmación.
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if usuario:
        db.delete(usuario)
        db.commit()

    return {"message": "Se eliminó usuario"}
