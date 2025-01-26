from fastapi import FastAPI, HTTPException
from utils import get_local_now_datetime
from db.models import Plan, Region, Comuna, ComunaOut, PlanComuna, Usuario, TipoUsuario
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
        raise HTTPException(status_code=400, detail="La comuna ya existe en el plan")
    
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
    return usuario