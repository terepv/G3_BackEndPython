from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Medida, Plan, PlanResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import PlanCreate, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/planes", tags=["Planes"])


@router.get(
    "/",
    response_model=list[PlanResponse],
    response_model_exclude_none=True,
    summary="Obtener todos los planes",
)
def read_planes(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """ Devuelve una lista de todos los planes.
    
    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.

    En caso de ser un organismo sectorial, solo podra acceder a los planes que le corresponden emitir un reporte.
    """
    if user.rol.rol == RolesEnum.ORGANISMO_SECTORIAL:
        planes = (
            db.query(PlanResponse)
            .join(Medida, PlanResponse.id_plan == Medida.id_plan)
            .filter(
                PlanResponse.eliminado_por == None,
                Medida.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
            )
            .all()
        )
    else:
        planes = db.query(PlanResponse).filter(PlanResponse.eliminado_por == None).all()
    return planes


@router.post(
    "/", 
    summary="Añade un plan", 
    status_code=201,
    response_model_exclude_none=True,
)
def add_plan(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    plan: PlanCreate = Body(
        openapi_examples={
            "default": get_example("plan_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega un plan.
    
    Argumentos:
    - nombre del plan (str)
    - descripción del plan (str)
    - fecha de publicación del plan (datetime)
    - id usuario (int)

    Devuelve un mensaje de confirmación con el recurso actualizado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    if db.query(Plan).filter(Plan.nombre.ilike(plan.nombre)).first():
        raise HTTPException(status_code=409, detail="Plan ya existe")

    data = PlanResponse(
        nombre=plan.nombre,
        descripcion=plan.descripcion,
        fecha_publicacion=plan.fecha_publicacion,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return {"message": "Se creó plan", "plan": data}

@router.put(
    "/{id_plan}",
    summary="Actualiza un plan por su id",
    response_model_exclude_none=True,
)
def update_plan(
    id_plan: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    plan: PlanCreate = Body(
        openapi_examples={
            "default": get_example("plan_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza un plan por su id.

    Argumentos:
    - nombre del plan (str)
    - descripción del plan (str)
    - fecha de publicación del plan (datetime)

    Devuelve mensaje de confirmación con el recurso actualizado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    data = db.query(PlanResponse).filter(PlanResponse.id_plan == id_plan, PlanResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe plan con ese id")
    if db.query(PlanResponse).filter(PlanResponse.id_plan != id_plan, PlanResponse.nombre.ilike(plan.nombre)).first():
        raise HTTPException(status_code=409, detail="Plan ya existe")
    data.nombre = plan.nombre
    data.descripcion = plan.descripcion
    data.fecha_publicacion = plan.fecha_publicacion
    data.fecha_actualizacion = get_local_now_datetime()
    data.actualizado_por = user.email
    db.commit()
    return (
        {"message": "Se actualizó plan", "plan": data}
    )


@router.delete(
    "/{id_plan}",
    summary="Elimina un plan por su id",
)
def delete_plan(
    id_plan: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina un plan por su id.

    Argumentos:
    - id del plan (int)

    Devuelve mensaje de confirmación con el recurso eliminado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    plan = db.query(PlanResponse).filter(PlanResponse.id_plan == id_plan, PlanResponse.eliminado_por == None).first()
    if plan:
        plan.fecha_eliminacion = get_local_now_datetime()
        plan.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó plan"}


@router.get(
    "/{id_plan}",
    response_model=PlanResponse,
    response_model_exclude_none=True,
    summary="Obtener un plan por su id",
)
def read_plan(
    id_plan: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un plan por su id.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.

    En caso de ser un organismo sectorial, solo podra acceder a los planes que le corresponden emitir un reporte.
    """
    if user.rol.rol == RolesEnum.ORGANISMO_SECTORIAL:
        plan = (
            db.query(PlanResponse)
            .join(Medida, PlanResponse.id_plan == Medida.id_plan)
            .filter(
                PlanResponse.eliminado_por == None,
                PlanResponse.id_plan == id_plan,
                Medida.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
            )
            .first()
        )
    else:
        plan = db.query(PlanResponse).filter(PlanResponse.id_plan == id_plan, PlanResponse.eliminado_por == None).first()

    if not plan:
        raise HTTPException(status_code=404, detail="No existe plan con ese id")
    return plan
