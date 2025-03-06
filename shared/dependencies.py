from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
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

async def get_user_email_from_token(
    token: Annotated[str | None, Depends(token_header_security)],
) -> str:
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
    return payload["email"]


async def get_user_from_db(
    db: AsyncDbSessionDep,
    user_email: str = Depends(get_user_email_from_token),
) -> UsuarioOut:
    usuario_exec = await db.execute(
        select(Usuario).where(Usuario.email == user_email)
    )
    usuario_db = usuario_exec.scalar_one_or_none()
    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no existe"
        )
    return usuario_db
