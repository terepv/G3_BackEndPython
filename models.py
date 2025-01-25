# PPDA models
from pydantic import BaseModel, List

class ComunaModel(BaseModel):
    id_comuna: int
    nombre_comuna: str
    id_region: int

    class Config:
        orm_mode = True


class RegionModel(BaseModel):
    id_region: int
    region: str
    
    class Config:
        orm_mode = True


class PlanModel(BaseModel):
    id_plan: int
    nombre: str
    descripcion: str
    id_usuario_creacion: int
    fecha_creacion: str

    class Config:
        orm_mode = True


class ComunaSchema(ComunaModel):
    plans: List[RegionModel]


class PlanSchema(PlanModel):
    comunas: List[ComunaModel]


class UsuarioModel(BaseModel):
    id_usuario: int
    nombre: str
    apellido: str
    email: str
    activo: bool
    id_tipo_usuario: int

    class Config:
        orm_mode = True


class TipoUsuarioModel(BaseModel):
    id_tipo_usuario: int
    tipo_usuario: str

    class Config:
        orm_mode = True


class OrganismoSectorial(BaseModel):
    id_organismo_sectorial: int
    organismo_sectorial: str

    class Config:
        orm_mode = True

