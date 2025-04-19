from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.db.models import Usuario
from app.shared.dependencies import SyncDbSessionDep, get_data_from_token, get_user_from_token_data
from app.shared.schemas import UsuarioOut
from app.shared.utils import create_access_token, create_refresh_token, get_local_now_datetime, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/token",
    summary="Obtener token de autenticación",
    description="Devuelve un token de acceso",
)
def get_token(
    db: SyncDbSessionDep,
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
):
    email = credentials.username
    password = credentials.password

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    data = {
        "sub": str(user.id_usuario),
        "iat": get_local_now_datetime(),
        "type": "access",
        "user": {
            "id_usuario": user.id_usuario,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "email": user.email,
            "rol": {
                "id_rol": user.id_rol,
                "rol": user.rol.rol,
            },
            "organismo_sectorial": {
                "id_organismo_sectorial": user.organismo_sectorial.id_organismo_sectorial,
                "organismo_sectorial": user.organismo_sectorial.organismo_sectorial,
            } if user.organismo_sectorial else None,
        }
    }
    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)
    return {
        "token_type": "bearer",
        "access_token": access_token, 
        "refresh_token": refresh_token
    }

@router.post(
    "/refresh",
    summary="Refrescar token de autenticación",
    description="Devuelve un nuevo token de acceso",
)
def get_refresh_token(
    token: dict | None = Depends(get_data_from_token)
):
    if token["type"] != "refresh":
        raise HTTPException(status_code=401, detail="El token provisto no es un token de refresco")
    new_data = token.copy()
    new_data.update({"iat": get_local_now_datetime()})
    new_data.update({"type": "access"})
    access_token = create_access_token(data=new_data)
    return {
        "token_type": "bearer",
        "access_token": access_token
    }

@router.get(
    "/me",
    summary="Obtener información del usuario autenticado",
    description="Devuelve información del usuario autenticado",
    response_model_exclude_none=True,
)
def read_users_me(
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
):
    return {"usuario_autenticado": user}