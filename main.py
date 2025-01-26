from fastapi import FastAPI, HTTPException
from utils import get_local_now_datetime
from db.models import Frecuencia, Medida, Opcion, Opcion_Medida, Plan, Region, Comuna, ComunaOut, PlanComuna, TipoDato, TipoMedida, Usuario, TipoUsuario, OrganismoSectorial
from shared.dependencies import SyncDbSessionDep

app = FastAPI(
    title="REST API REPORTES PPDA",
    description=f"Last deployment: {get_local_now_datetime()}",
)

@app.get("/")
def read_root():
    return {"Hello": "World Ivan"}

@app.get("/regiones", response_model=list[Region], tags=["regiones"], summary="Obtener todas las regiones")
def read_regions(
    db: SyncDbSessionDep,
):
    regions = db.query(Region).all()
    return regions

@app.get("/region/{id_region}", response_model=Region, tags=["regiones"], summary="Obtener una region por su id")
def read_region(
    id_region: int,
    db: SyncDbSessionDep,
):
    region = db.query(Region).filter(Region.id_region == id_region).first()
    if not region:
        raise HTTPException(status_code=404, detail="No existe región con ese id")
    return region

@app.get("/comunas", response_model=list[ComunaOut], tags=["comunas"], summary="Obtener todas las comunas")
def read_comunas(
    db: SyncDbSessionDep,
):
    comunas = db.query(Comuna).join(Region).all()
    return comunas

@app.get("/comuna/{id_comuna}", response_model=ComunaOut, tags=["comunas"], summary="Obtener una comuna por su id")
def read_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
):
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()
    if not comuna:
        raise HTTPException(status_code=404, detail="No existe comuna con ese id")
    return comuna

# Ejercicio planteado: endpoint para añadir comuna con sqlalchemy

@app.get("/planes", response_model=list[Plan], tags=["planes"], summary="Obtener todos los planes")
def read_planes(
    db: SyncDbSessionDep,
):
    planes = db.query(Plan).all()
    return planes

@app.get("/plan/{id_plan}", response_model=Plan, tags=["planes"], summary="Obtener un plan por su id")
def read_plan(
    id_plan: int,
    db: SyncDbSessionDep,
):
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    if not plan:
        raise HTTPException(status_code=404, detail="No existe plan con ese id")
    return plan

@app.get("/plan/{id_plan}/comunas", response_model=list[ComunaOut], tags=["planes"], summary="Obtener todas las comunas de un plan")
def read_planes_comunas(
    id_plan: int,
    db: SyncDbSessionDep,
):
    comunas = db.query(Comuna).join(PlanComuna).filter(PlanComuna.id_plan == id_plan).all()
    return comunas

@app.post("/plan/{id_plan}/comuna/{id_comuna}", tags=["planes"], summary="Agregar una comuna a un plan")
def add_comuna_to_plan(
    id_plan: int,
    id_comuna: int,
    db: SyncDbSessionDep,
):
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="El plan no existe")
    if not comuna:
        raise HTTPException(status_code=404, detail="La comuna no existe")
    
    if db.query(PlanComuna).filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna).first():
        raise HTTPException(status_code=409, detail="La comuna ya existe en el plan")
    
    plan_comuna = PlanComuna(id_plan=id_plan, id_comuna=id_comuna)
    db.add(plan_comuna)
    db.commit()
    db.refresh(plan_comuna)
    
    return {"message": "Se agregó la comuna al plan", "plan_comuna": plan_comuna}

@app.delete("/plan/{id_plan}/comuna/{id_comuna}", tags=["planes"], summary="Eliminar una comuna de un plan")
def delete_comuna_from_plan(
    id_plan: int,
    id_comuna: int,
    db: SyncDbSessionDep,
):
    if not db.query(PlanComuna).filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna).first():
        return {"message": "Se eliminó la comuna del plan"}
    
    plan_comuna = db.query(PlanComuna).filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna).first()
    db.delete(plan_comuna)
    db.commit()
    
    return {"message": "Se eliminó la comuna del plan"}

@app.get("/usuarios", response_model=list[Usuario], tags=["usuarios"], summary="Obtener todos los usuarios")
def read_users(
    db: SyncDbSessionDep,
):
    users = db.query(Usuario).all()
    return users

@app.get("/usuario/{id_usuario}", response_model=Usuario, tags=["usuarios"], summary="Obtener un usuario por su id")
def read_user(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    usuario = db.query(Usuario).filter(Usuario.id_tipo_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe usuario con ese id")
    return usuario

@app.get("/organismos_sectoriales", response_model=list[OrganismoSectorial], tags=["organismos sectoriales"], summary="Obtener todos los organismos sectoriales")
def read_organismos(
    db: SyncDbSessionDep,
):
    organismos = db.query(OrganismoSectorial).all()
    return organismos

@app.get("/organismo_sectorial/{id_organismo_sectorial}", response_model=OrganismoSectorial, tags=["organismos sectoriales"], summary="Obtener un organismo sectorial por su id")
def read_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
):
    organismo = db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first()
    if not organismo:
        raise HTTPException(status_code=404, detail="No existe organismo sectorial con ese id")
    return organismo

@app.post("/organismo_sectorial/", tags=["organismos sectoriales"], summary="Añade un organismo sectorial")
def add_organismo(
    organismo_sectorial: str,
    db: SyncDbSessionDep
):
    if not db.query(OrganismoSectorial).filter(OrganismoSectorial.organismo_sectorial==organismo_sectorial).first():
        organismo = OrganismoSectorial(organismo_sectorial=organismo_sectorial)
        db.add(organismo)
        db.commit()
        db.refresh(organismo)
        return {"message": "Se creó organismo sectorial", "organismo sectorial": organismo}
    
    return HTTPException(status_code=409, detail="Organismo Sectorial ya existe")

@app.delete("/organismo_sectorial/{id_organismo_sectorial}", tags=["organismos sectoriales"], summary="Elimina un organismo sectorial")
def delete_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
):
    if not db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first():
        return HTTPException(status_code=404, detail="Organismo Sectorial no existe")
    
    organismo = db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first()
    db.delete(organismo)
    db.commit()
    return {"message": "Se eliminó organismo sectorial", "organismo sectorial": organismo}

@app.get("/frecuencias", response_model=list[Frecuencia], tags=["frecuencias"], summary="Obtener todas las frecuencias")
def read_frecuencias(
    db: SyncDbSessionDep,
):
    frecuencias = db.query(Frecuencia).all()
    return frecuencias

@app.get("/frecuencia/{id_frecuencia}", response_model=Frecuencia, tags=["frecuencias"], summary="Obtener una frecuencia por su id")
def read_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
):
    frecuencia = db.query(Frecuencia).filter(Frecuencia.id_frecuencia==id_frecuencia).first()
    if not frecuencia:
        raise HTTPException(status_code=404, detail="No existe frecuencia con ese id")
    return frecuencia

@app.post("/frecuencia/", tags=["frecuencias"], summary="Añade una frecuencia")
def add_frecuencia(
    frecuencia: str,
    db: SyncDbSessionDep,
):
    frecuencia = Frecuencia(frecuencia=frecuencia)
    db.add(frecuencia)
    db.commit()
    db.refresh(frecuencia)
    return {"message": "Se creó frecuencia", "frecuencia": frecuencia}

@app.delete("/frecuencia/{id_frecuencia}", tags=["frecuencias"], summary="Elimina una frecuencia")
def delete_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
):
    frecuencia = db.query(Frecuencia).filter(Frecuencia.id_frecuencia==id_frecuencia).first()
    db.delete(frecuencia)
    db.commit()
    return {"message": "Se eliminó frecuencia", "frecuencia": frecuencia}

@app.get("/tipo_medidas", response_model=list[TipoMedida], tags=["tipo medidas"], summary="Obtener todos los tipos de medidas")
def read_tipo_medidas(
    db: SyncDbSessionDep,
):
    tipo_medidas = db.query(TipoMedida).all()
    return tipo_medidas

@app.get("/tipo_medida/{id_tipo_medida}", response_model=TipoMedida, tags=["tipo medidas"], summary="Obtener un tipo de medida por su id")
def read_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
):
    tipo_medida = db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==id_tipo_medida).first()
    if not tipo_medida:
        raise HTTPException(status_code=404, detail="No existe tipo de medida con ese id")
    return tipo_medida

@app.post("/tipo_medida/", tags=["tipo medidas"], summary="Añade un tipo de medida")
def add_tipo_medida(
    tipo_medida: str,
    db: SyncDbSessionDep,
):
    tipo_medida = TipoMedida(tipo_medida=tipo_medida)
    db.add(tipo_medida)
    db.commit()
    db.refresh(tipo_medida)
    return {"message": "Se creó tipo de medida", "tipo de medida": tipo_medida}

@app.delete("/tipo_medida/{id_tipo_medida}", tags=["tipo medidas"], summary="Elimina un tipo de medida")
def delete_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
):
    tipo_medida = db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==id_tipo_medida).first()
    db.delete(tipo_medida)
    db.commit()
    return {"message": "Se eliminó tipo de medida", "tipo de medida": tipo_medida}

@app.get("/tipos_datos", response_model=list[TipoDato], tags=["tipo datos"], summary="Obtener todos los tipos de datos")
def read_tipo_datos(
    db: SyncDbSessionDep,
):
    tipo_datos = db.query(TipoDato).all()
    return tipo_datos

@app.get("/opciones_medidas", response_model=list[Opcion_Medida], tags=["opciones medidas"], summary="Obtener todas las opciones de medidas")
def read_opciones_medidas(
    db: SyncDbSessionDep,
):
    opciones_medidas = db.query(Opcion_Medida).all()
    return opciones_medidas

@app.post("/opcion_medida", tags=["opciones medidas"], summary="Añade una opcion de medida")
def add_opcion_medida(
    id_opcion: int,
    id_medida: int,
    db: SyncDbSessionDep,
):
    if not db.query(Opcion).filter(Opcion.id_opcion==id_opcion).first():
        raise HTTPException(status_code=404, detail="Opcion no existe")
    if not db.query(Medida).filter(Medida.id_medida==id_medida).first():
        raise HTTPException(status_code=404, detail="Medida no existe")
    
    opcion_medida = Opcion_Medida(id_opcion=id_opcion, id_medida=id_medida)
    db.add(opcion_medida)
    db.commit()
    db.refresh(opcion_medida)
    return {"message": "Se creó opcion de medida", "opcion de medida": opcion_medida}

@app.delete("/opcion_medida/{id_opcion_medida}", tags=["opciones medidas"], summary="Elimina una opcion de medida")
def delete_opcion_medida(
    id_opcion_medida: int,
    db: SyncDbSessionDep,
): 
    opcion_medida = db.query(Opcion_Medida).filter(Opcion_Medida.id_opcion_medida==id_opcion_medida).first()
    db.delete(opcion_medida)
    db.commit()
    return {"message": "Se eliminó opcion de medida", "opcion de medida": opcion_medida}

@app.get("/opciones", response_model=list[Opcion], tags=["opciones"], summary="Obtener todas las opciones")
def read_opciones(
    db: SyncDbSessionDep,
):
    opciones = db.query(Opcion).all()
    return opciones

@app.post("/opcion", tags=["opciones"], summary="Añade una opcion")
def add_opcion(
    opcion: str,
    db: SyncDbSessionDep,
):
    opcion = Opcion(opcion=opcion)
    db.add(opcion)
    db.commit()
    db.refresh(opcion)
    return {"message": "Se creó opcion", "opcion": opcion}

@app.delete("/opcion/{id_opcion}", tags=["opciones"], summary="Elimina una opcion")
def delete_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
):
    opcion = db.query(Opcion).filter(Opcion.id_opcion==id_opcion).first()
    db.delete(opcion)
    db.commit()
    return {"message": "Se eliminó opcion", "opcion": opcion}

@app.get("/medidas", response_model=list[Medida], tags=["medidas"], summary="Obtener todas las medidas")
def read_medidas(
    db:SyncDbSessionDep,
):
    medidas = db.query(Medida).all()
    return medidas

@app.get("/medida/{id_medida}", response_model=Medida, tags=["medidas"], summary="Obtener una medida por su id")
def read_medida(
    id_medida: int,
    db: SyncDbSessionDep,
):
    medida = db.query(Medida).filter(Medida.id_medida == id_medida).first()
    if not medida:
        raise HTTPException(status_code=404, detail="No existe medida con ese id")
    return medida

# TODO Falta implementar endpoints de medida (POST, DELETE)