from datetime import date, datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    text
)
from shared.utils import get_local_now_datetime

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class AuditMixin(MappedAsDataclass):
    fecha_creacion: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        init=False,
        nullable=False,
        default_factory=get_local_now_datetime,
        server_default=text("(CURRENT_TIMESTAMP)"),
        repr=False,
    )
    creado_por: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        repr=False,
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        init=False,
        repr=False,
    )
    actualizado_por: Mapped[str | None] = mapped_column(
        String(255),
        init=False,
        repr=False,
    )
    fecha_eliminacion: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        init=False,
        repr=False,
    )
    eliminado_por: Mapped[str | None] = mapped_column(
        String(255),
        init=False,
        repr=False,
    )

    class Config:
        orm_mode = True

class Rol(Base):
    __tablename__ = "rol"
    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rol: Mapped[str] = mapped_column(String(50), nullable=False)

class OrganismoSectorial(Base):
    __tablename__ = "organismo_sectorial"
    id_organismo_sectorial: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organismo_sectorial: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __init__(self, organismo_sectorial: str):
        self.organismo_sectorial = organismo_sectorial

class OrganismoSectorialResponse(OrganismoSectorial, AuditMixin):
    def __init__(self, organismo_sectorial: str, fecha_creacion: datetime | None = None, creado_por: str | None = None):
        self.organismo_sectorial = organismo_sectorial
        self.fecha_creacion = fecha_creacion
        self.creado_por = creado_por

class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    id_rol: Mapped[int] = mapped_column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    rol: Mapped[Rol] = relationship(Rol)
    id_organismo_sectorial: Mapped[int | None] = mapped_column(Integer, ForeignKey("organismo_sectorial.id_organismo_sectorial"), nullable=True)
    organismo_sectorial: Mapped["OrganismoSectorial"] = relationship(OrganismoSectorial)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    
    def __init__(self, nombre: str, apellido: str, email: str, password: str, id_rol: int, id_organismo_sectorial: int | None, activo: bool = True):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password
        self.id_rol = id_rol
        self.activo = activo
        self.id_organismo_sectorial = id_organismo_sectorial

class Region(Base):
    __tablename__ = "region"
    id_region: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    class Config:
        orm_mode = True

class RegionResponse(Region, AuditMixin):
    def __init__(self, region: str, fecha_creacion: datetime | None = None, creado_por: str | None = None):
        self.region = region
        self.fecha_creacion = fecha_creacion
        self.creado_por = creado_por
    

class Comuna(Base):
    __tablename__ = "comuna"
    id_comuna: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comuna: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    id_region: Mapped[int] = mapped_column(Integer, ForeignKey("region.id_region"), nullable=False)
    region: Mapped[Region] = relationship(Region)

class ComunaResponse(Comuna, AuditMixin):
    def __init__(self, comuna: str, id_region: int, fecha_creacion: datetime | None = None, creado_por: str | None = None):
        self.comuna = comuna
        self.id_region = id_region
        self.fecha_creacion = fecha_creacion
        self.creado_por = creado_por

class Plan(Base):
    __tablename__ = "plan"
    id_plan: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_publicacion: Mapped[date] = mapped_column(Date, nullable=False, default=datetime.now())

    def __init__(self, nombre: str, descripcion: str, fecha_publicacion: datetime | None = None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_publicacion = fecha_publicacion or datetime.now()

    class Config:
        orm_mode = True

class PlanResponse(Plan, AuditMixin):
    def __init__(self, nombre: str, descripcion: str, fecha_publicacion: datetime | None = None, fecha_creacion: datetime | None = None, creado_por: str | None = None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_publicacion = fecha_publicacion or datetime.now()
        self.fecha_creacion = fecha_creacion
        self.creado_por = creado_por

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

class PlanComunaResponse(PlanComuna, AuditMixin):
    def __init__(self, id_plan: int, id_comuna: int, fecha_creacion: datetime | None = None, creado_por: str | None = None):
        self.id_plan = id_plan
        self.id_comuna = id_comuna
        self.fecha_creacion = fecha_creacion
        self.creado_por = creado_por

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
    reporte_unico: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __init__(self, nombre_corto: str, indicador: str, formula_calculo: str, id_frecuencia: int, id_organismo_sectorial: int, id_tipo_medida: int, id_plan: int, desc_medio_de_verificacion: str, id_tipo_dato: int, reporte_unico: bool):
        self.nombre_corto = nombre_corto
        self.indicador = indicador
        self.formula_calculo = formula_calculo
        self.id_frecuencia = id_frecuencia
        self.id_organismo_sectorial = id_organismo_sectorial
        self.id_tipo_medida = id_tipo_medida
        self.id_plan = id_plan
        self.desc_medio_de_verificacion = desc_medio_de_verificacion
        self.id_tipo_dato = id_tipo_dato
        self.reporte_unico = reporte_unico

class MedidaResponse(Medida, AuditMixin):
    def __init__(self, nombre_corto: str, indicador: str, formula_calculo: str, id_frecuencia: int, id_organismo_sectorial: int, id_tipo_medida: int, id_plan: int, desc_medio_de_verificacion: str, id_tipo_dato: int, reporte_unico: bool, fecha_creacion: datetime | None = None, creado_por: str | None = None):
        self.nombre_corto = nombre_corto
        self.indicador = indicador
        self.formula_calculo = formula_calculo
        self.id_frecuencia = id_frecuencia
        self.id_organismo_sectorial = id_organismo_sectorial
        self.id_tipo_medida = id_tipo_medida
        self.id_plan = id_plan
        self.desc_medio_de_verificacion = desc_medio_de_verificacion
        self.id_tipo_dato = id_tipo_dato
        self.reporte_unico = reporte_unico
        self.fecha_creacion = fecha_creacion
        self.creado_por = creado_por

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

class Reporte(Base):
    __tablename__ = "reporte"
    id_reporte: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_medida: Mapped[int] = mapped_column(Integer, ForeignKey("medida.id_medida"), nullable=False)
    medida: Mapped[Medida] = relationship(Medida)
    id_usuario_creacion: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    usuario_creacion: Mapped[Usuario] = relationship(Usuario)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, id_medida: int, id_usuario_creacion: int, fecha_registro: datetime | None = None):
        self.id_medida = id_medida
        self.id_usuario_creacion = id_usuario_creacion
        self.fecha_registro = fecha_registro or datetime.now()

class OrganismoSectorialUsuario(Base):
    __tablename__ = "organismo_sectorial_usuario"
    id_organismo_sectorial_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_organismo_sectorial: Mapped[int] = mapped_column(Integer, ForeignKey("organismo_sectorial.id_organismo_sectorial"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    organismo_sectorial: Mapped[OrganismoSectorial] = relationship(OrganismoSectorial)
    usuario: Mapped[Usuario] = relationship(Usuario)

class MedioVerificacion(Base):
    __tablename__ = "medio_verificacion"
    id_reporte: Mapped[int] = mapped_column(Integer, ForeignKey("reporte.id_reporte"), primary_key=True, nullable=False)
    reporte: Mapped[Reporte] = relationship(Reporte)
    nombre_archivo: Mapped[str] = mapped_column(String(100), nullable=False)
    archivo: Mapped[bytes] = mapped_column(String(100), nullable=False)
    tamano: Mapped[int] = mapped_column(Integer, nullable=False)