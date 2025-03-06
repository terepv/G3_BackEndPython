from fastapi import FastAPI
from routes import (
    auth, comunas, frecuencias, opciones, opciones_medidas, organismos_sectoriales, planes, planes_medidas, 
    regiones, planes_comuna, tipo_medidas, tipos_datos, usuarios
)
from shared.utils import get_local_now_datetime

app = FastAPI(
    title="REST API REPORTES PPDA",
    description=f"Last deployment: {get_local_now_datetime()}",
)

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(auth.router)
app.include_router(regiones.router)
app.include_router(comunas.router)
app.include_router(planes.router)
app.include_router(planes_comuna.router)
app.include_router(planes_medidas.router)
app.include_router(usuarios.router)
app.include_router(organismos_sectoriales.router)
app.include_router(frecuencias.router)
app.include_router(tipo_medidas.router)
app.include_router(tipos_datos.router)
app.include_router(opciones.router)
app.include_router(opciones_medidas.router)





