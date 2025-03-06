from fastapi import APIRouter, Form, HTTPException
from pydantic import Field

from db.models import Usuario
from shared.dependencies import SyncDbSessionDep
from shared.utils import create_access_token, get_local_now_datetime


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/token",
    summary="Obtener token de autenticación",
    description="Devuelve un token de autenticación",
)
def read_comunas(
    db: SyncDbSessionDep,
    email: str = Form(...),
    password: str = Form(...),
):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not user.password == password:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    data = {
        "sub": str(user.id_usuario),
        "name": f"{user.nombre} {user.apellido}",
        "given_name": user.nombre,
        "family_name": user.apellido,
        "email": user.email,
        "groups": [user.tipo_usuario.tipo_usuario],
        "iat": get_local_now_datetime()
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}
