from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT
)

db_connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db_connection_string_async = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    db_connection_string,
    pool_size=5,
    pool_pre_ping=True,
    max_overflow=0,
    pool_recycle=1800,
    echo=False,
)
SessionDep = sessionmaker(autoflush=False, autocommit=False, bind=engine)

engine_async = create_async_engine(
    db_connection_string_async,
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