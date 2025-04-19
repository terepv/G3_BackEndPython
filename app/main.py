from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.routes import (
    auth, comunas
    , frecuencias
    , opciones
    , opciones_medidas
    , organismos_sectoriales, planes, planes_medidas
    , regiones, planes_comuna, roles, tipo_medidas, usuarios, reportes
    , tipos_datos
)
from app.shared.utils import get_local_now_datetime

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app = FastAPI(
    title="REST API REPORTES PPDA",
    description=f"Last deployment: {get_local_now_datetime()}",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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
app.include_router(reportes.router)
app.include_router(roles.router)

def run_uvicorn():
    import argparse
    import uvicorn

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--port", type=int, default=8000)
    args = argparser.parse_args()

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=args.port,
        reload=True,
    )


if __name__ == "__main__":
    run_uvicorn()
