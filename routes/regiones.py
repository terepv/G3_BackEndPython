from fastapi import APIRouter, HTTPException
from db.models import Region
from shared.dependencies import SyncDbSessionDep

router = APIRouter(prefix="/regiones", tags=["Regiones"])

@router.get("/", response_model=list[Region], summary="Obtener todas las regiones")
def read_regions(
    db: SyncDbSessionDep,
):
    regions = db.query(Region).all()
    return regions

@router.get("/{id_region}", response_model=Region, summary="Obtener una region por su id")
def read_region(
    id_region: int,
    db: SyncDbSessionDep,
):
    region = db.query(Region).filter(Region.id_region == id_region).first()
    if not region:
        raise HTTPException(status_code=404, detail="No existe región con ese id")
    return region