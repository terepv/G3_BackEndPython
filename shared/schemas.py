from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class BaseModelCustom(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
        extra="ignore",
    )

class TipoUsuario(BaseModelCustom):
    id_tipo_usuario: int
    tipo_usuario: str

class UsuarioCreate(BaseModelCustom):
    nombre: str
    apellido: str
    email: str
    password: str
    activo: bool | None = True
    id_tipo_usuario: int

class UsuarioOut(BaseModelCustom):
    id_usuario: int
    nombre: str
    apellido: str
    email: str
    tipo_usuario: TipoUsuario

class Region(BaseModelCustom):
    id_region: int
    region: str

class ComunaOut(BaseModelCustom):
    id_comuna: int
    comuna: str
    region: Region

class PlanCreate(BaseModelCustom):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=3, max_length=100)
    fecha_publicacion: datetime

class OrganismoSectorialCreate(BaseModelCustom):
    organismo_sectorial: str = Field(..., min_length=3, max_length=100)

class FrecuenciaCreate(BaseModelCustom):
    frecuencia: str = Field(..., min_length=3, max_length=100)

class TipoMedidaCreate(BaseModelCustom):
    tipo_medida: str = Field(..., min_length=3, max_length=100)

class OpcionCreate(BaseModelCustom):
    opcion: str = Field(..., min_length=1, max_length=100)

class MedidaCreate(BaseModelCustom):
    nombre_corto: str
    indicador: str
    formula_calculo: str
    id_frecuencia: int
    id_organismo_sectorial: int
    id_tipo_medida: int
    desc_medio_de_verificacion: str
    id_tipo_dato: int
    cron: str | None
    reporte_unico: bool

class MedidaOut(BaseModelCustom):
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
    cron: str | None
    reporte_unico: bool

class Opcion(BaseModelCustom):
    id_opcion: int
    opcion: str

class OpcionMedidaCreate(BaseModelCustom):
    id_opcion: int
    id_medida: int

class OpcionMedidaOut(BaseModelCustom):
    id_opcion_medida: int
    opcion: Opcion
    medida: MedidaOut