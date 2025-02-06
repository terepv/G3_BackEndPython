from fastapi import FastAPI, Body, HTTPException


from api_examples import get_example
from utils import get_local_now_datetime
from db.models import (
      Frecuencia, FrecuenciaCreate, Medida, MedidaCreate, MedidaOut, Opcion, OpcionCreate, OpcionMedida
    , OpcionMedidaCreate, OpcionMedidaOut, OrganismoSectorialCreate, Plan, PlanCreate, Region, Comuna, ComunaOut
    , PlanComuna, TipoDato, TipoMedida, TipoMedidaCreate, TipoUsuario, Usuario, OrganismoSectorial, UsuarioCreate, UsuarioOut
)
from shared.dependencies import SyncDbSessionDep

app = FastAPI(
    title="REST API REPORTES PPDA",
    description=f"Last deployment: {get_local_now_datetime()}",
)

@app.get("/regiones", response_model=list[Region], tags=["regiones"], summary="Obtener todas las regiones")
def read_regions(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las regiones. """
    regions = db.query(Region).all()
    return regions

@app.get("/region/{id_region}", response_model=Region, tags=["regiones"], summary="Obtener una region por su id")
def read_region(
    id_region: int,
    db: SyncDbSessionDep,
):
    """ 
    Devuelve una región por su id. 
    Argumentos:
    - id región (int)
    """
    region = db.query(Region).filter(Region.id_region == id_region).first()
    if not region:
        raise HTTPException(status_code=404, detail="No existe región con ese id")
    return region

@app.get("/comunas", response_model=list[ComunaOut], tags=["comunas"], summary="Obtener todas las comunas")
def read_comunas(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las comunas. """
    comunas = db.query(Comuna).join(Region).all()
    return comunas

@app.get("/comuna/{id_comuna}", response_model=ComunaOut, tags=["comunas"], summary="Obtener una comuna por su id")
def read_comuna(
    id_comuna: int,
    db: SyncDbSessionDep,
):
    """
    Devuelve una comuna por su id. 
    Argumentos: 
    - id de comuna (int)
    """
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()
    if not comuna:
        raise HTTPException(status_code=404, detail="No existe comuna con ese id")
    return comuna

@app.get("/planes", response_model=list[Plan], tags=["planes"], summary="Obtener todos los planes")
def read_planes(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todos los planes. """
    planes = db.query(Plan).all()
    return planes

@app.post("/plan", tags=["planes"], summary="Añade un plan", status_code=201)
def add_plan(
    db: SyncDbSessionDep,
    plan: PlanCreate = Body(
        openapi_examples={
            "default": get_example("plan_post"),
        }
    ),
):
    """ Agrega un plan a la base de datos.
    Argumentos:
    - nombre del plan (str)
    - descripción del plan (str)
    - fecha publicación del plan (datetime) 
    - id usuario (int)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    if db.query(Plan).filter(Plan.nombre.ilike(plan.nombre)).first():
        raise HTTPException(status_code=409, detail="Plan ya existe")
    
    data = Plan(
        nombre=plan.nombre, 
        descripcion=plan.descripcion, 
        fecha_publicacion=plan.fecha_publicacion,
        id_usuario_creacion=1
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    
    return {"message": "Se creó plan", "plan": data}

@app.delete("/plan/{id_plan}", tags=["planes"], summary="Elimina un plan por su id")
def delete_plan(
    id_plan: int,
    db: SyncDbSessionDep,
):
    """
    Elimina un plan por su id.
    Argumentos: 
    - id de plan (int)

    Devuelve mensaje de confirmación.
    """
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    if plan:
        db.delete(plan)
        db.commit()
    return {"message": "Se eliminó plan"}


@app.get("/plan/{id_plan}", response_model=Plan, tags=["planes"], summary="Obtener un plan por su id")
def read_plan(
    id_plan: int,
    db: SyncDbSessionDep,
):
    """
    Devuelve un plan por su id
    Argumentos: 
    - id de plan. (int)
    """
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    if not plan:
        raise HTTPException(status_code=404, detail="No existe plan con ese id")
    return plan

@app.get("/plan/{id_plan}/comunas", response_model=list[ComunaOut], tags=["planes"], summary="Obtener todas las comunas de un plan")
def read_planes_comunas(
    id_plan: int,
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las comunas de un plan. """
    comunas = db.query(Comuna).join(PlanComuna).filter(PlanComuna.id_plan == id_plan).all()
    return comunas

@app.post("/plan/{id_plan}/comuna/{id_comuna}", tags=["planes"], summary="Agregar una comuna a un plan", status_code=201)
def add_comuna_to_plan(
    id_plan: int,
    id_comuna: int,
    db: SyncDbSessionDep,
):
    """
    Agrega una comuna a un plan.
    Argumentos:
    - id_plan (int)
    - id_comuna (int)

    Devuelve mensaje de confirmación con el recurso creado.
    """
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
    """
    Elimina una comuna de un plan, por su id.
    Argumentos:
    - id plan (int)
    - id comuna (int)

    Devuelve mensaje de confirmación.
    """
    if not db.query(PlanComuna).filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna).first():
        return {"message": "Se eliminó la comuna del plan"}
    
    plan_comuna = db.query(PlanComuna).filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna).first()
    db.delete(plan_comuna)
    db.commit()
    
    return {"message": "Se eliminó la comuna del plan"}

@app.get("/plan/{id_plan}/medidas", response_model=list[MedidaOut], tags=["planes"], summary="Obtener todas las medidas de un plan")
def read_planes_medidas(
    id_plan: int,
    db: SyncDbSessionDep,
):
    """
    Devuelve una lista con todas las medidas asociadas a un plan.
    Argumentos: 
    - id plan (int)
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="El plan no existe")
    
    medidas = db.query(Medida).filter(Medida.id_plan == id_plan).all()
    return medidas

@app.post("/plan/{id_plan}/medida", tags=["planes"], summary="Agregar una medida a un plan", status_code=201)
def add_medida(
    db: SyncDbSessionDep,
    id_plan: int,
    medida: MedidaCreate = Body(
        openapi_examples={
            "default": get_example("medida_post"),
        }
    ),
):
    """
    Agrega una medida a un plan.
    Argumentos:
    - id del plan (int)
    - nombre corto medida (str)
    - indicador de la medida (str)
    - id frecuencia de la medida (int)
    - id organismo sectorial (int)
    - id tipo de medida (int)
    - descripción medio de verificación (str)
    - id tipo de dato (int)
    - cron (str)
    - reporte unico (bool)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    data = Medida(
        nombre_corto=medida.nombre_corto, 
        indicador=medida.indicador, 
        formula_calculo=medida.formula_calculo, 
        id_frecuencia=medida.id_frecuencia, 
        id_organismo_sectorial=medida.id_organismo_sectorial, 
        id_tipo_medida=medida.id_tipo_medida, 
        id_plan=id_plan, 
        desc_medio_de_verificacion=medida.desc_medio_de_verificacion, 
        id_tipo_dato=medida.id_tipo_dato, 
        cron=medida.cron, 
        reporte_unico=medida.reporte_unico
    )

    if not db.query(Plan).filter(Plan.id_plan==id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    if db.query(Medida).filter(Medida.nombre_corto.ilike(data.nombre_corto)).first():
        raise HTTPException(status_code=409, detail="Medida ya existe")
    if not db.query(Frecuencia).filter(Frecuencia.id_frecuencia==data.id_frecuencia).first():
        raise HTTPException(status_code=404, detail="Frecuencia no existe")
    if not db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==data.id_organismo_sectorial).first():
        raise HTTPException(status_code=404, detail="Organismo sectorial no existe")
    if not db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==data.id_tipo_medida).first():
        raise HTTPException(status_code=404, detail="Tipo de medida no existe")
    if not db.query(TipoDato).filter(TipoDato.id_tipo_dato==data.id_tipo_dato).first():
        raise HTTPException(status_code=404, detail="Tipo de dato no existe")
    
    db.add(data)
    db.commit()
    db.refresh(data)
    medida_out = MedidaOut(**data.__dict__)
    return {"message": "Se creó medida", "medida": medida_out}

@app.put("/plan/{id_plan}/medida/{id_medida}", tags=["planes"], summary="Actualizar una medida de un plan")
def update_medida(
    db: SyncDbSessionDep,
    id_plan: int,
    id_medida: int,
    medida: MedidaCreate = Body(
        openapi_examples={
            "default": get_example("medida_post"),
        }
    ),
):
    """
    Actualiza una medida de un plan.
    Argumentos:
    - id del plan (int) 
    - id de medida (int)
    - nombre corto medida (str)
    - indicador de la medida (str)
    - id frecuencia de la medida (int)
    - id organismo sectorial (int)
    - id tipo de medida (int)
    - descripción medio de verificación (str)
    - id tipo de dato (int)
    - cron (str)
    - reporte unico (bool)

    Devuelve mensaje de confirmación con el recurso actualizado.
    """
    if not db.query(Plan).filter(Plan.id_plan==id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    
    medida_db = db.query(Medida).filter(Medida.id_medida == id_medida).first()
    if not medida_db:
        raise HTTPException(status_code=404, detail="Medida no existe")
    
    if not db.query(Medida).filter(Medida.id_medida==id_medida).first():
        raise HTTPException(status_code=404, detail="Medida no existe")
    if not db.query(Frecuencia).filter(Frecuencia.id_frecuencia==medida.id_frecuencia).first():
        raise HTTPException(status_code=404, detail="Frecuencia no existe")
    if not db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==medida.id_organismo_sectorial).first():
        raise HTTPException(status_code=404, detail="Organismo sectorial no existe")
    if not db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==medida.id_tipo_medida).first():
        raise HTTPException(status_code=404, detail="Tipo de medida no existe")
    if not db.query(TipoDato).filter(TipoDato.id_tipo_dato==medida.id_tipo_dato).first():
        raise HTTPException(status_code=404, detail="Tipo de dato no existe")
    
    medida_db.nombre_corto = medida.nombre_corto
    medida_db.indicador = medida.indicador
    medida_db.formula_calculo = medida.formula_calculo
    medida_db.id_frecuencia = medida.id_frecuencia
    medida_db.id_organismo_sectorial = medida.id_organismo_sectorial
    medida_db.id_tipo_medida = medida.id_tipo_medida
    medida_db.id_plan = id_plan
    medida_db.desc_medio_de_verificacion = medida.desc_medio_de_verificacion
    medida_db.id_tipo_dato = medida.id_tipo_dato
    medida_db.cron = medida.cron
    medida_db.reporte_unico = medida.reporte_unico

    db.commit()
    db.refresh(medida_db)

    medida_out = MedidaOut(**medida_db.__dict__)
    
    return {"message": "Se actualizó la medida", "medida": medida_out}

@app.delete("/plan/{id_plan}/medida/{id_medida}", tags=["planes"], summary="Elimina una medida de un plan por su id")
def delete_medida(
    id_plan: int,
    id_medida: int,
    db: SyncDbSessionDep,
):
    """
    Elimina una medida de un plan por su id.
    Argumentos:
    - id plan (int)
    - id medida (int)

    Devuelve mensaje de confirmación.
    """
    if not db.query(Plan).filter(Plan.id_plan==id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    medida = db.query(Medida).filter(Medida.id_medida==id_medida).first()
    if medida:
        db.delete(medida)
        db.commit()
    return {"message": "Se eliminó medida"}


@app.get("/usuarios", response_model=list[UsuarioOut], tags=["usuarios"], summary="Obtener todos los usuarios")
def read_users(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todos los usuarios. """
    users = db.query(Usuario).all()
    return users

@app.get("/usuario/{id_usuario}", response_model=Usuario, tags=["usuarios"], summary="Obtener un usuario por su id")
def read_user(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    """ 
    Devuelve un usuario por su id.
    Argumentos: 
    - id usuario (int)
    """
    usuario = db.query(Usuario).filter(Usuario.id_tipo_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe usuario con ese id")
    return usuario

@app.post("/usuario", tags=["usuarios"], summary="Añade un usuario", status_code=201)
def add_user(
    db: SyncDbSessionDep,
    usuario: UsuarioCreate = Body(
        openapi_examples={
            "default": get_example("usuario_post"),
        }
    ),
):
    """
    Agrega un usuario. 
    Argumentos:
    - nombre (str)
    - apellido (str)
    - email (str)
    - usuario activo (bool)
    - id tipo de usuario (int)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    if db.query(Usuario).filter(Usuario.email.ilike(usuario.email)).first():
        raise HTTPException(status_code=409, detail="Usuario ya existe")
    if not db.query(TipoUsuario).filter(TipoUsuario.id_tipo_usuario==usuario.id_tipo_usuario).first():
        raise HTTPException(status_code=404, detail="Tipo de usuario no existe")

    data = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email, 
        activo=usuario.activo,
        id_tipo_usuario=usuario.id_tipo_usuario
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message": "Se creó el usuario", "usuario": data}

@app.delete("/usuario/{id_usuario}", tags=["usuarios"], summary="Elimina un usuario por su id")
def delete_usuario(
    id_usuario: int,
    db: SyncDbSessionDep,
):
    """
    Elimina un usuario por su id.
    Argumentos: 
    - id usuario (int)

    Devuelve mensaje de confirmación.
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario==id_usuario).first()
    if usuario:
        db.delete(usuario)
        db.commit()

    return {"message": "Se eliminó usuario"}


@app.get("/organismos_sectoriales", response_model=list[OrganismoSectorial], tags=["organismos sectoriales"], summary="Obtener todos los organismos sectoriales")
def read_organismos(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todos los organismos sectoriales. """
    organismos = db.query(OrganismoSectorial).all()
    return organismos

@app.get("/organismo_sectorial/{id_organismo_sectorial}", response_model=OrganismoSectorial, tags=["organismos sectoriales"], summary="Obtener un organismo sectorial por su id")
def read_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
):
    """
    Devuelve un organismo sectorial por su id.
    Argumentos: 
    - id organismo sectorial (int)
    """
    organismo = db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first()
    if not organismo:
        raise HTTPException(status_code=404, detail="No existe organismo sectorial con ese id")
    return organismo

@app.post("/organismo_sectorial", tags=["organismos sectoriales"], summary="Añade un organismo sectorial", status_code=201)
def add_organismo(
    db: SyncDbSessionDep,
    organismo_sectorial: OrganismoSectorialCreate = Body(
        openapi_examples={
            "default": get_example("organismo_sectorial_post"),
        }
    ),
):
    """
    Agrega un organismo sectorial a la base de datos.
    Argumentos:
    - organismo sectorial (str).

    Devuelve mensaje de confirmación con el recurso creado.
    """
    nombre_organismo_sectorial = organismo_sectorial.organismo_sectorial
    if db.query(OrganismoSectorial).filter(OrganismoSectorial.organismo_sectorial.ilike(nombre_organismo_sectorial)).first():
        raise HTTPException(status_code=409, detail="Organismo sectorial ya existe")
    
    if len(nombre_organismo_sectorial) < 3:
        raise HTTPException(status_code=400, detail="Nombre de organismo sectorial muy corto")
    if len(nombre_organismo_sectorial) > 100:
        raise HTTPException(status_code=400, detail="Nombre de organismo sectorial muy largo")

    
    organismo = OrganismoSectorial(organismo_sectorial=nombre_organismo_sectorial)
    db.add(organismo)
    db.commit()
    db.refresh(organismo)
    return {"message": "Se creó organismo sectorial", "organismo_sectorial": organismo}

@app.delete("/organismo_sectorial/{id_organismo_sectorial}", tags=["organismos sectoriales"], summary="Elimina un organismo sectorial")
def delete_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
):
    """
    Elimina un organismo sectorial por su id.
    Argumentos:
    - id organismo sectorial (int)
    
    Devuelve mensaje de confirmación.
    """
    organismo = db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first()
    if organismo:
        db.delete(organismo)
        db.commit()
    
    return {"message": "Se eliminó organismo sectorial"}

@app.get("/frecuencias", response_model=list[Frecuencia], tags=["frecuencias"], summary="Obtener todas las frecuencias")
def read_frecuencias(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las frecuencias. """
    frecuencias = db.query(Frecuencia).all()
    return frecuencias

@app.get("/frecuencia/{id_frecuencia}", response_model=Frecuencia, tags=["frecuencias"], summary="Obtener una frecuencia por su id")
def read_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
):
    """
    Devuelve una frecuencia por su id.
    Argumentos:
    - id frecuencia (int)
    """
    frecuencia = db.query(Frecuencia).filter(Frecuencia.id_frecuencia==id_frecuencia).first()
    if not frecuencia:
        raise HTTPException(status_code=404, detail="No existe frecuencia con ese id")
    return frecuencia

@app.post("/frecuencia", tags=["frecuencias"], summary="Añade una frecuencia", status_code=201)
def add_frecuencia(
    db: SyncDbSessionDep,
    frecuencia: FrecuenciaCreate = Body(
        openapi_examples={
            "default": get_example("frecuencia_post"),
        }
    ),
):
    """
    Agrega una frecuencia a la base de datos.
    Argumentos:
    - frecuencia (str)
    
    Devuelve mensaje de confirmación con el recurso creado.
    """
    nombre_frecuencia = frecuencia.frecuencia
    if db.query(Frecuencia).filter(Frecuencia.frecuencia.ilike(nombre_frecuencia)).first():
        raise HTTPException(status_code=409, detail="Frecuencia ya existe")
    if len(nombre_frecuencia) < 3:
        raise HTTPException(status_code=400, detail="Nombre de frecuencia muy corto")
    if len(nombre_frecuencia) > 100:
        raise HTTPException(status_code=400, detail="Nombre de frecuencia muy largo")

    frecuencia = Frecuencia(frecuencia=nombre_frecuencia)
    db.add(frecuencia)
    db.commit()
    db.refresh(frecuencia)
    return {"message": "Se creó frecuencia", "frecuencia": frecuencia}

@app.delete("/frecuencia/{id_frecuencia}", tags=["frecuencias"], summary="Elimina una frecuencia")
def delete_frecuencia(
    id_frecuencia: int,
    db: SyncDbSessionDep,
):
    """
    Elimina una frecuencia por su id.
    Argumentos:
    - id frecuencia (int)
    
    Devuelve mensaje de confirmación.
    """
    frecuencia = db.query(Frecuencia).filter(Frecuencia.id_frecuencia==id_frecuencia).first()
    if frecuencia:
        db.delete(frecuencia)
        db.commit()
    return {"message": "Se eliminó frecuencia"}

@app.get("/tipo_medidas", response_model=list[TipoMedida], tags=["tipo medidas"], summary="Obtener todos los tipos de medidas")
def read_tipo_medidas(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todos los tipos de medidas. """
    tipo_medidas = db.query(TipoMedida).all()
    return tipo_medidas

@app.get("/tipo_medida/{id_tipo_medida}", response_model=TipoMedida, tags=["tipo medidas"], summary="Obtener un tipo de medida por su id")
def read_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
):
    """ 
    Devuelve un tipo de medida por su id.
    Argumentos:
    - id tipo de medida (int)
    """
    tipo_medida = db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==id_tipo_medida).first()
    if not tipo_medida:
        raise HTTPException(status_code=404, detail="No existe tipo de medida con ese id")
    return tipo_medida

@app.post("/tipo_medida/", tags=["tipo medidas"], summary="Añade un tipo de medida", status_code=201)
def add_tipo_medida(
    db: SyncDbSessionDep,
    tipo_medida: TipoMedidaCreate = Body(
        openapi_examples={
            "default": get_example("tipo_medida_post"),
        }
    ),
):
    """
    Agrega un tipo de medida a la base de datos.
    Argumentos:
    - tipo de medida (str)
    
    Devuelve mensaje de confirmación con el recurso creado.
    """
    nombre_tipo_medida = tipo_medida.tipo_medida
    
    if db.query(TipoMedida).filter(TipoMedida.tipo_medida.ilike(nombre_tipo_medida)).first():
        raise HTTPException(status_code=409, detail="Tipo de medida ya existe")
    if len(nombre_tipo_medida) < 3:
        raise HTTPException(status_code=400, detail="Nombre de tipo de medida muy corto")
    if len(nombre_tipo_medida) > 100:
        raise HTTPException(status_code=400, detail="Nombre de tipo de medida muy largo")
    
    tipo_medida = TipoMedida(tipo_medida=nombre_tipo_medida)
    db.add(tipo_medida)
    db.commit()
    db.refresh(tipo_medida)
    return {"message": "Se creó tipo de medida", "tipo de medida": tipo_medida}

@app.delete("/tipo_medida/{id_tipo_medida}", tags=["tipo medidas"], summary="Elimina un tipo de medida")
def delete_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
):
    """
    Elimina un tipo de medida por su id.
    Argumentos:
    - id tipo de medida (int)

    Devuelve mensaje de confirmación.
    """
    tipo_medida = db.query(TipoMedida).filter(TipoMedida.id_tipo_medida==id_tipo_medida).first()
    if tipo_medida:
        db.delete(tipo_medida)
        db.commit()
    return {"message": "Se eliminó tipo de medida"}

@app.get("/tipos_datos", response_model=list[TipoDato], tags=["tipo datos"], summary="Obtener todos los tipos de datos")
def read_tipo_datos(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista de todos los tipos de datos. """
    tipo_datos = db.query(TipoDato).all()
    return tipo_datos

@app.get("/opciones_medidas", response_model=list[OpcionMedidaOut], tags=["opciones medidas"], summary="Obtener todas las opciones de medidas")
def read_opciones_medidas(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las asociaciones de opciones y medidas. """
    opciones_medidas = db.query(OpcionMedida).join(Medida).join(Opcion).all()
    return opciones_medidas

@app.post("/opcion_medida", tags=["opciones medidas"], summary="Añade una opcion de medida", status_code=201)
def add_opcion_medida(
    db: SyncDbSessionDep,
    opcion_medida: OpcionMedidaCreate = Body(
        openapi_examples={
            "default": get_example("opcion_medida_post"),
        }
    ),
):
    """
    Agrega una relación de opción y medida a la base de datos.
    Argumentos:
    - id opción (int)
    - id medida (int)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    opcion = db.query(Opcion).filter(Opcion.id_opcion==opcion_medida.id_opcion).first()
    if not opcion:
        raise HTTPException(status_code=404, detail="Opcion no existe")
    medida = db.query(Medida).filter(Medida.id_medida==opcion_medida.id_medida).first()
    if not medida:
        raise HTTPException(status_code=404, detail="Medida no existe")
    if db.query(OpcionMedida).filter(OpcionMedida.id_opcion==opcion_medida.id_opcion, OpcionMedida.id_medida==opcion_medida.id_medida).first():
        raise HTTPException(status_code=409, detail="Opcion de medida ya existe")
    
    opcion_medida = OpcionMedida(id_opcion=opcion_medida.id_opcion, id_medida=opcion_medida.id_medida)
    db.add(opcion_medida)
    db.commit()
    db.refresh(opcion_medida)
    opcion_medida_out = OpcionMedidaOut(id_opcion_medida=opcion_medida.id_opcion_medida, opcion=opcion, medida=medida)
    return {"message": "Se creó opcion de medida", "opcion_medida": opcion_medida_out}

@app.delete("/opcion_medida/{id_opcion_medida}", tags=["opciones medidas"], summary="Elimina una opcion de medida")
def delete_opcion_medida(
    id_opcion_medida: int,
    db: SyncDbSessionDep,
): 
    """
    Elimina una relación de opción-medida por su id.
    Argumentos:
    - id opción de medida (int)
    
    Devuelve mensaje de confirmación.
    """
    opcion_medida = db.query(OpcionMedida).filter(OpcionMedida.id_opcion_medida==id_opcion_medida).first()
    if opcion_medida:
        db.delete(opcion_medida)
        db.commit()
    return {"message": "Se eliminó opcion de medida"}

@app.get("/opciones", response_model=list[Opcion], tags=["opciones"], summary="Obtener todas las opciones")
def read_opciones(
    db: SyncDbSessionDep,
):
    """ Devuelve una lista con todas las opciones. """
    opciones = db.query(Opcion).all()
    return opciones

@app.post("/opcion", tags=["opciones"], summary="Añade una opcion", status_code=201)
def add_opcion(
    db: SyncDbSessionDep,
    opcion: OpcionCreate = Body(
        openapi_examples={
            "default": get_example("opcion_post"),
        }
    ),
):
    """
    Agrega una opción a la base de datos.
    Argumentos:
    - opción (str)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    nombre_opcion = opcion.opcion
    if db.query(Opcion).filter(Opcion.opcion.ilike(nombre_opcion)).first():
        raise HTTPException(status_code=409, detail="Opcion ya existe")
    if len(opcion.opcion) == 0:
        raise HTTPException(status_code=400, detail="Opcion no puede ser vacío")
    if len(opcion.opcion) > 100:
        raise HTTPException(status_code=400, detail="Opcion muy larga")
    
    opcion = Opcion(opcion=nombre_opcion)
    db.add(opcion)
    db.commit()
    db.refresh(opcion)
    return {"message": "Se creó opcion", "opcion": opcion}

@app.delete("/opcion/{id_opcion}", tags=["opciones"], summary="Elimina una opción")
def delete_opcion(
    id_opcion: int,
    db: SyncDbSessionDep,
):
    """
    Elimina una opción por su id.
    Argumentos:
    - id opción (int)
    
    Devuelve mensaje de confirmación.
    """
    opcion = db.query(Opcion).filter(Opcion.id_opcion==id_opcion).first()
    if opcion:
        db.delete(opcion)
        db.commit()
    return {"message": "Se eliminó opción"}
