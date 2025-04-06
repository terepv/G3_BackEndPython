from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from db.models import Comuna, MedidaResponse, Plan, PlanComunaResponse, PlanResponse
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import UsuarioOut
from shared.utils import get_local_now_datetime

router = APIRouter(prefix="/planes/{id_plan}/comunas", tags=["Planes - Comunas"])


@router.get(
    "/",
    response_model=list[PlanComunaResponse],
    response_model_exclude_none=True,
    summary="Obtener todas las comunas de un plan",
)
def read_planes_comunas(
    id_plan: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las comunas asociadas a un plan.
    
    Argumentos:
    - id plan (int)
    
    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    if user.rol.rol == RolesEnum.ORGANISMO_SECTORIAL:
        plan_comunas = (
            db.query(PlanComunaResponse)
            .join(PlanResponse, PlanResponse.id_plan == PlanComunaResponse.id_plan)
            .join(MedidaResponse, MedidaResponse.id_plan == PlanResponse.id_plan)
            .filter(
                PlanResponse.eliminado_por == None,
                MedidaResponse.eliminado_por == None,
                PlanComunaResponse.eliminado_por == None,
                MedidaResponse.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
            )
            .all()
        )
    else:
        plan_comunas = db.query(PlanComunaResponse).filter(PlanComunaResponse.id_plan == id_plan, PlanComunaResponse.eliminado_por == None).all()
    return plan_comunas


@router.post(
    "/{id_comuna}",
    summary="Agregar una comuna a un plan",
    status_code=201,
    response_model_exclude_none=True,
)
def add_comuna_to_plan(
    id_plan: int,
    id_comuna: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega una comuna a un plan.
    
    Argumentos:
    - id plan (int)
    - id comuna (int)
    
    Devuelve un mensaje de confirmación con el recurso creado.
    
    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()

    if not plan:
        raise HTTPException(status_code=404, detail="El plan no existe")
    if not comuna:
        raise HTTPException(status_code=404, detail="La comuna no existe")
    
    if db.query(PlanComunaResponse).filter(
        PlanComunaResponse.id_plan == id_plan, 
        PlanComunaResponse.id_comuna == id_comuna, 
        PlanComunaResponse.eliminado_por == None
    ).first():
        raise HTTPException(status_code=409, detail="La comuna ya está asociada al plan")

    plan_comuna = PlanComunaResponse(id_plan=id_plan, id_comuna=id_comuna, creado_por=user.email, fecha_creacion=get_local_now_datetime())
    db.add(plan_comuna)
    db.commit()
    db.refresh(plan_comuna)

    return {"message": "Se agregó la comuna al plan", "plan_comuna": plan_comuna}


@router.delete(
    "/{id_plan_comuna}",
    summary="Eliminar una comuna de un plan",
)
def delete_comuna_from_plan(
    id_plan: int,
    id_plan_comuna: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una comuna de un plan.
    
    Argumentos:
    - id del plan (int)
    - id del plan comuna (int)

    Devuelve un mensaje de confirmación.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """

    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="El plan no existe")

    plan_comuna = db.query(PlanComunaResponse).filter(PlanComunaResponse.id_plan_comuna == id_plan_comuna).first()

    if plan_comuna:
        plan_comuna.fecha_eliminacion = get_local_now_datetime()
        plan_comuna.eliminado_por = user.email
        db.commit()

    return {"message": "Se eliminó la comuna del plan"}
