from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Plan
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum
from shared.schemas import PlanCreate
from shared.utils import get_example

router = APIRouter(prefix="/planes", tags=["Planes"])


@router.get(
    "/",
    response_model=list[Plan],
    summary="Obtener todos los planes",
)
def read_planes(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """ Devuelve una lista de todos los planes.
    
    Requiere estar autenticado con rol de SMA u Organismo Sectorial para acceder a este recurso.
    """
    planes = db.query(Plan).all()
    return planes


@router.post("/", summary="Añade un plan", status_code=201)
def add_plan(
    db: SyncDbSessionDep,
    plan: PlanCreate = Body(
        openapi_examples={
            "default": get_example("plan_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Agrega un plan.
    
    Argumentos:
    - nombre del plan (str)
    - descripción del plan (str)
    - fecha de publicación del plan (datetime)
    - id usuario (int)

    Devuelve mensaje de confirmación con el recurso creado.

    Requiere estar autenticado con rol de SMA para acceder a este recurso.
    """
    if db.query(Plan).filter(Plan.nombre.ilike(plan.nombre)).first():
        raise HTTPException(status_code=409, detail="Plan ya existe")

    data = Plan(
        nombre=plan.nombre,
        descripcion=plan.descripcion,
        fecha_publicacion=plan.fecha_publicacion,
        id_usuario_creacion=1,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return {"message": "Se creó plan", "plan": data}


@router.delete(
    "/{id_plan}",
    summary="Elimina un plan por su id",
)
def delete_plan(
    id_plan: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Elimina un plan por su id.

    Argumentos:
    - id del plan (int)

    Devuelve mensaje de confirmación con el recurso eliminado.

    Requiere estar autenticado con rol de SMA para acceder a este recurso.
    """
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    if plan:
        db.delete(plan)
        db.commit()
    return {"message": "Se eliminó plan"}


@router.get(
    "/{id_plan}",
    response_model=Plan,
    summary="Obtener un plan por su id",
)
def read_plan(
    id_plan: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un plan por su id.

    Requiere estar autenticado con rol de SMA o Organismo Sectorial para acceder a este recurso.
    """
    plan = db.query(Plan).filter(Plan.id_plan == id_plan).first()
    if not plan:
        raise HTTPException(status_code=404, detail="No existe plan con ese id")
    return plan
