from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db.models import Usuario
from shared.dependencies import SyncDbSessionDep, get_data_from_token
from shared.utils import create_access_token, create_refresh_token, get_local_now_datetime, verify_password


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
            "tipo_usuario": {
                "id_tipo_usuario": user.id_tipo_usuario,
                "tipo_usuario": user.tipo_usuario.tipo_usuario,
            },
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