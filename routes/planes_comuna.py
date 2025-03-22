from fastapi import APIRouter, Depends, HTTPException
from db.models import Comuna, Plan, PlanComuna
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum
from shared.schemas import ComunaOut

router = APIRouter(prefix="/planes/{id_plan}/comunas", tags=["Planes - Comunas"])


@router.get(
    "/",
    response_model=list[ComunaOut],
    summary="Obtener todas las comunas de un plan",
)
def read_planes_comunas(
    id_plan: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las comunas asociadas a un plan.
    
    Argumentos:
    - id plan (int)
    
    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """
    comunas = (
        db.query(Comuna).join(PlanComuna).filter(PlanComuna.id_plan == id_plan).all()
    )
    return comunas


@router.post(
    "/{id_comuna}",
    summary="Agregar una comuna a un plan",
    status_code=201,
)
def add_comuna_to_plan(
    id_plan: int,
    id_comuna: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Agrega una comuna a un plan.
    
    Argumentos:
    - id plan (int)
    - id comuna (int)
    
    Devuelve un mensaje de confirmación con el recurso creado.
    
    Requiere ser usuario de SMA para acceder a este recurso.
    """
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    comuna = db.query(Comuna).filter(Comuna.id_comuna == id_comuna).first()

    if not plan:
        raise HTTPException(status_code=404, detail="El plan no existe")
    if not comuna:
        raise HTTPException(status_code=404, detail="La comuna no existe")

    if (
        db.query(PlanComuna)
        .filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna)
        .first()
    ):
        raise HTTPException(status_code=409, detail="La comuna ya existe en el plan")

    plan_comuna = PlanComuna(id_plan=id_plan, id_comuna=id_comuna)
    db.add(plan_comuna)
    db.commit()
    db.refresh(plan_comuna)

    return {"message": "Se agregó la comuna al plan", "plan_comuna": plan_comuna}


@router.delete(
    "/{id_comuna}",
    summary="Eliminar una comuna de un plan",
)
def delete_comuna_from_plan(
    id_plan: int,
    id_comuna: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Elimina una comuna de un plan.
    
    Argumentos:
    - id del plan (int)
    - id de la comuna (int)

    Devuelve un mensaje de confirmación.

    Requiere estar autenticado con rol de SMA para acceder a este recurso.
    """
    if (
        not db.query(PlanComuna)
        .filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna)
        .first()
    ):
        return {"message": "Se eliminó la comuna del plan"}

    plan_comuna = (
        db.query(PlanComuna)
        .filter(PlanComuna.id_plan == id_plan, PlanComuna.id_comuna == id_comuna)
        .first()
    )
    db.delete(plan_comuna)
    db.commit()

    return {"message": "Se eliminó la comuna del plan"}
