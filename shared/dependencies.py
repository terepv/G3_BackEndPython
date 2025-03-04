from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import SessionDep
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def get_db():
    db = SessionDep()
    try:
        yield db
    finally:
        db.close()


SyncDbSessionDep = Annotated[Session, Depends(get_db)]

security = HTTPBasic()

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"Fido"
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"Fido123"
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong user o password!",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True