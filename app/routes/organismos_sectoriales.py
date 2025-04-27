from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from app.db.models import OrganismoSectorialResponse
from app.shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from app.shared.enums import RolesEnum
from app.shared.schemas import OrganismoSectorialCreate, UsuarioOut
from app.shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/organismos_sectoriales", tags=["Organismos Sectoriales"])


@router.get(
    "/",
    response_model=list[OrganismoSectorialResponse],
    response_model_exclude_none=True,
    summary="Obtener todos los organismos sectoriales",
)
def read_organismos(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todos los organismos sectoriales.
    
    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    organismos = db.query(OrganismoSectorialResponse).filter(OrganismoSectorialResponse.eliminado_por == None).all()
    return organismos


@router.get(
    "/{id_organismo_sectorial}",
    response_model=OrganismoSectorialResponse,
    summary="Obtener un organismo sectorial por su id",
)
def read_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un organismo sectorial por su id.

    Argumentos:
    - id_organismo_sectorial: El id del organismo sectorial a obtener.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    organismo = (
        db.query(OrganismoSectorialResponse)
        .filter(OrganismoSectorialResponse.id_organismo_sectorial == id_organismo_sectorial, OrganismoSectorialResponse.eliminado_por == None)
        .first()
    )
    if not organismo:
        raise HTTPException(
            status_code=404, detail="No existe organismo sectorial con ese id"
        )
    return organismo


@router.post(
        "/", 
        summary="Añade un organismo sectorial", 
        status_code=201,
        response_model_exclude_none=True,
)
def add_organismo(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    organismo_sectorial: OrganismoSectorialCreate = Body(
        openapi_examples={
            "default": get_example("organismo_sectorial_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega un organismo sectorial a la base de datos.
    
    Argumentos:
    - organismo_sectorial: El nombre del organismo sectorial a agregar.

    Devuelve mensaje de confirmación con el recurso creado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    nombre_organismo_sectorial = organismo_sectorial.organismo_sectorial
    if (
        db.query(OrganismoSectorialResponse)
        .filter(
            OrganismoSectorialResponse.organismo_sectorial.ilike(nombre_organismo_sectorial),
            OrganismoSectorialResponse.eliminado_por == None
        )
        .first()
    ):
        raise HTTPException(status_code=409, detail="Organismo sectorial ya existe")

    if len(nombre_organismo_sectorial) < 3:
        raise HTTPException(
            status_code=400, detail="Nombre de organismo sectorial muy corto"
        )
    if len(nombre_organismo_sectorial) > 100:
        raise HTTPException(
            status_code=400, detail="Nombre de organismo sectorial muy largo"
        )

    organismo = OrganismoSectorialResponse(
        organismo_sectorial=nombre_organismo_sectorial,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )
    db.add(organismo)
    db.commit()
    db.refresh(organismo)
    return {"message": "Se creó organismo sectorial", "organismo_sectorial": organismo}


@router.put(
    "/{id_organismo_sectorial}",
    summary="Actualiza un plan por su id",
    response_model_exclude_none=True,
)
def update_organismo_sectorial(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    organismo_sectorial: OrganismoSectorialCreate = Body(
        openapi_examples={
            "default": get_example("organismo_sectorial_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza un organismo sectorial por su id.

    Argumentos:
    - organismo_sectorial: El nombre del organismo sectorial a agregar.

    Devuelve mensaje de confirmación con el recurso actualizado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    data = db.query(OrganismoSectorialResponse).filter(OrganismoSectorialResponse.id_organismo_sectorial == id_organismo_sectorial, OrganismoSectorialResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe organismo sectorial con ese id")
    if db.query(OrganismoSectorialResponse).filter(OrganismoSectorialResponse.id_organismo_sectorial != id_organismo_sectorial, OrganismoSectorialResponse.organismo_sectorial.ilike(organismo_sectorial.organismo_sectorial)).first():
        raise HTTPException(status_code=409, detail="Organismo sectorial ya existe")
    data.organismo_sectorial = organismo_sectorial.organismo_sectorial
    data.fecha_actualizacion = get_local_now_datetime()
    data.actualizado_por = user.email
    db.commit()
    return (
        {"message": "Se actualizó organismo sectorial", "organismo_sectorial": data}
    )

@router.delete(
    "/{id_organismo_sectorial}",
    summary="Elimina un organismo sectorial",
)
def delete_organismo(
    id_organismo_sectorial: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina un organismo sectorial de la base de datos.

    Argumentos:
    - id_organismo_sectorial: El id del organismo sectorial a eliminar.

    Devuelve mensaje de confirmación.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    organismo = db.query(OrganismoSectorialResponse).filter(OrganismoSectorialResponse.id_organismo_sectorial == id_organismo_sectorial, OrganismoSectorialResponse.eliminado_por == None).first()
    if organismo:
        organismo.fecha_eliminacion = get_local_now_datetime()
        organismo.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó organismo sectorial"}
