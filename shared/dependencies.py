from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

# from config import TOKEN_ALGORITHM, TOKEN_SECRET_KEY
from config import TOKEN_ALGORITHM, TOKEN_SECRET_KEY
from db.database import SessionDep, SessionDepAsync
from db.models import Usuario
from shared.schemas import UsuarioOut

def get_db():
    with SessionDep() as db:
        yield db


SyncDbSessionDep = Annotated[Session, Depends(get_db)]

async def get_db_async():
    async with SessionDepAsync() as db:
        yield db


AsyncDbSessionDep = Annotated[AsyncSession, Depends(get_db_async)]

token_header_security = APIKeyHeader(name="Authorization", auto_error=False)

def get_data_from_token(
    token: Annotated[str | None, Depends(token_header_security)],
) -> dict:
    """
    Recibe un token por Header y devuelve el email del usuario que realiz la peticion.
    Si el token es invalido o no existe, devuelve un HTTPException con status 401.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas"
        )
    try:
        payload = jwt.decode(
            token.split(" ")[1],
            TOKEN_SECRET_KEY,
            algorithms=[TOKEN_ALGORITHM],
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido"
        )
    return payload


def get_user_from_token_data(
    data: dict = Depends(get_data_from_token),
) -> UsuarioOut:
    """
    Recibe el payload del token de acceso y devuelve el usuario que realiza la petición.
    Si el token es invalido, no existe o no es del tipo adecuado, devuelve un HTTPException con status 401.
    """
    if data["type"] != "access":
        raise HTTPException(status_code=401, detail="El token provisto no es un token de acceso")
    
    return UsuarioOut(**data["user"])

class RoleChecker:  
  def __init__(self, allowed_roles):  
    self.allowed_roles = allowed_roles  
  
  def __call__(self, user: Annotated[UsuarioOut, Depends(get_user_from_token_data)]):  
    if user.tipo_usuario.tipo_usuario in self.allowed_roles:  
      return True  
    raise HTTPException(  
       status_code=status.HTTP_401_UNAUTHORIZED,   
       detail="No tiene permisos para acceder a este recurso"
    )  