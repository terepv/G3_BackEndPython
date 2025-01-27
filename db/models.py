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
    Boolean,
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
    region: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)


class Comuna(Base):
    __tablename__ = "comuna"
    id_comuna: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comuna: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
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
    fecha_publicacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

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

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: str
    apellido: str
    email: str
    tipo_usuario: TipoUsuario
    class Config:
        from_attributes = True

class OrganismoSectorial(Base):
    __tablename__ = "organismo_sectorial"
    id_organismo_sectorial: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organismo_sectorial: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __init__(self, organismo_sectorial: str):
        self.organismo_sectorial = organismo_sectorial

class Frecuencia(Base):
    __tablename__ = "frecuencia"
    id_frecuencia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frecuencia: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __init__(self, frecuencia: str):
        self.frecuencia = frecuencia

class TipoMedida(Base):
    __tablename__ = "tipo_medida"
    id_tipo_medida: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_medida: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __init__(self, tipo_medida: str):
        self.tipo_medida = tipo_medida

class TipoDato(Base):
    __tablename__ = "tipo_dato"
    id_tipo_dato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_dato: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __init__(self, tipo_dato: str):
        self.tipo_dato = tipo_dato

class Opcion(Base):
    __tablename__ = "opcion"
    id_opcion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    opcion: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, opcion: str):
        self.opcion = opcion

class Medida(Base):
    __tablename__ = "medida"
    id_medida: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_corto: Mapped[str] = mapped_column(String(100), nullable=False)
    indicador: Mapped[str] = mapped_column(String(100), nullable=False)
    formula_calculo: Mapped[str] = mapped_column(String(100), nullable=False)
    id_frecuencia: Mapped[int] = mapped_column(Integer, ForeignKey("frecuencia.id_frecuencia"), nullable=False)
    frecuencia: Mapped[Frecuencia] = relationship(Frecuencia)
    id_organismo_sectorial: Mapped[int] = mapped_column(Integer, ForeignKey("organismo_sectorial.id_organismo_sectorial"), nullable=False)
    organismo_sectorial: Mapped[OrganismoSectorial] = relationship(OrganismoSectorial)
    id_tipo_medida: Mapped[int] = mapped_column(Integer, ForeignKey("tipo_medida.id_tipo_medida"), nullable=False)
    tipo_medida: Mapped[TipoMedida] = relationship(TipoMedida)
    id_plan: Mapped[int] = mapped_column(Integer, ForeignKey("plan.id_plan"), nullable=False)
    plan: Mapped[Plan] = relationship(Plan)
    desc_medio_de_verificacion: Mapped[str] = mapped_column(String(100), nullable=False)
    id_tipo_dato: Mapped[int] = mapped_column(Integer, ForeignKey("tipo_dato.id_tipo_dato"), nullable=False)
    tipo_dato: Mapped[TipoDato] = relationship(TipoDato)
    cron: Mapped[str] = mapped_column(String(100), nullable=False)
    reporte_unico: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __init__(self, nombre_corto: str, indicador: str, formula_calculo: str, id_frecuencia: int, id_organismo_sectorial: int, id_tipo_medida: int, id_plan: int, desc_medio_de_verificacion: str, id_tipo_dato: int, cron: str, reporte_unico: bool):
        self.nombre_corto = nombre_corto
        self.indicador = indicador
        self.formula_calculo = formula_calculo
        self.id_frecuencia = id_frecuencia
        self.id_organismo_sectorial = id_organismo_sectorial
        self.id_tipo_medida = id_tipo_medida
        self.id_plan = id_plan
        self.desc_medio_de_verificacion = desc_medio_de_verificacion
        self.id_tipo_dato = id_tipo_dato
        self.cron = cron
        self.reporte_unico = reporte_unico

class MedidaOut(BaseModel):
    id_medida: int
    nombre_corto: str
    indicador: str
    formula_calculo: str
    id_frecuencia: int
    id_organismo_sectorial: int
    id_tipo_medida: int
    id_plan: int
    desc_medio_de_verificacion: str
    id_tipo_dato: int
    cron: str
    reporte_unico: bool
    class Config:
        from_attributes = True

class OpcionMedida(Base):
    __tablename__ = "opcion_medida"
    id_opcion_medida: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_opcion: Mapped[int] = mapped_column(Integer, ForeignKey("opcion.id_opcion"), nullable=False)
    id_medida: Mapped[int] = mapped_column(Integer, ForeignKey("medida.id_medida"), nullable=False)
    opcion: Mapped[Opcion] = relationship(Opcion)
    medida: Mapped[Medida] = relationship(Medida)

    def __init__(self, id_opcion: int, id_medida: int):
        self.id_opcion = id_opcion
        self.id_medida = id_medida

class OpcionMedidaOut(BaseModel):
    id_opcion_medida: int
    opcion: Opcion
    medida: MedidaOut
    class Config:
        from_attributes = True
