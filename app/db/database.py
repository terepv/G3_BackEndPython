from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_CONNECTION_STRING, DB_CONNECTION_STRING_ASYNC

engine = create_engine(
    DB_CONNECTION_STRING,
    pool_size=5,
    pool_pre_ping=True,
    max_overflow=0,
    pool_recycle=1800,
    echo=False,
)
SessionDep = sessionmaker(autoflush=False, autocommit=False, bind=engine)

engine_async = create_async_engine(
    DB_CONNECTION_STRING_ASYNC,
    pool_size=5,
    pool_pre_ping=True,
    max_overflow=0,
    pool_recycle=1800,
    echo=False,
)
SessionDepAsync = async_sessionmaker(
    engine_async,
    class_=AsyncSession,
    autoflush=False, autocommit=False, expire_on_commit=False
)