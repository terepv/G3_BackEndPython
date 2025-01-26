from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy import (
    DateTime,
    Integer,
    String,
    ForeignKey,
)

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class Region(Base):
    __tablename__ = "region"
    id_region: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region: Mapped[str] = mapped_column(String(100), nullable=False)


class Comuna(Base):
    __tablename__ = "comuna"
    id_comuna: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comuna: Mapped[str] = mapped_column(String(100), nullable=False)
    id_region: Mapped[int] = mapped_column(Integer, ForeignKey("region.id_region"), nullable=False)
    region: Mapped[Region] = relationship(Region)

class ComunaOut(BaseModel):
    id_comuna: int
    comuna: str
    region: Region
    class Config:
        from_attributes = True

class Plan(Base):
    __tablename__ = "plan"
    id_plan: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_publicacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class PlanComuna(Base):
    __tablename__ = "plan_comuna"
    id_plan_comuna: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_plan: Mapped[int] = mapped_column(Integer, ForeignKey("plan.id_plan"), nullable=False)
    id_comuna: Mapped[int] = mapped_column(Integer, ForeignKey("comuna.id_comuna"), nullable=False)
    plan: Mapped[Plan] = relationship(Plan)
    comuna: Mapped[Comuna] = relationship(Comuna)
    
    def __init__(self, id_plan: int, id_comuna: int):
        self.id_plan = id_plan
        self.id_comuna = id_comuna

class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"
    id_tipo_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_usuario: Mapped[str] = mapped_column(String(50), nullable=False)


class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    id_tipo_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("tipo_usuario.id_tipo_usuario"), nullable=False)
    tipo_usuario: Mapped[TipoUsuario] = relationship(TipoUsuario)

class OrganismoSectorial(Base):
    __tablename__ = "organismo_sectorial"
    id_organismo_sectorial: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organismo_sectorial: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, organismo_sectorial: str):
        self.organismo_sectorial = organismo_sectorial

class Frecuencia(Base):
    __tablename__ = "frecuencia"
    id_frecuencia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frecuencia: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, frecuencia: str):
        self.frecuencia = frecuencia

class TipoMedida(Base):
    __tablename__ = "tipo_medida"
    id_tipo_medida: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_medida: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, tipo_medida: str):
        self.tipo_medida = tipo_medida

