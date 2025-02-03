from fastapi import APIRouter, Body, HTTPException
from db.models import OrganismoSectorial
from shared.dependencies import SyncDbSessionDep
from shared.schemas import OrganismoSectorialCreate
from shared.utils import get_example

router = APIRouter(prefix="/organismos_sectoriales", tags=["Organismos Sectoriales"])

@router.get("/", response_model=list[OrganismoSectorial], summary="Obtener todos los organismos sectoriales")
def read_organismos(
    db: SyncDbSessionDep,
):
    organismos = db.query(OrganismoSectorial).all()
    return organismos

@router.get("/{id_organismo_sectorial}", response_model=OrganismoSectorial, summary="Obtener un organismo sectorial por su id")
def read_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
):
    organismo = db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first()
    if not organismo:
        raise HTTPException(status_code=404, detail="No existe organismo sectorial con ese id")
    return organismo

@router.post("/", summary="Añade un organismo sectorial", status_code=201)
def add_organismo(
    db: SyncDbSessionDep,
    organismo_sectorial: OrganismoSectorialCreate = Body(
        openapi_examples={
            "default": get_example("organismo_sectorial_post"),
        }
    ),
):
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

@router.delete("/{id_organismo_sectorial}", summary="Elimina un organismo sectorial")
def delete_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
):
    organismo = db.query(OrganismoSectorial).filter(OrganismoSectorial.id_organismo_sectorial==id_organismo_sectorial).first()
    if organismo:
        db.delete(organismo)
        db.commit()
    
    return {"message": "Se eliminó organismo sectorial"}