from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import SessionDep


def get_db():
    db = SessionDep()
    try:
        yield db
    finally:
        db.close()


SyncDbSessionDep = Annotated[Session, Depends(get_db)]
