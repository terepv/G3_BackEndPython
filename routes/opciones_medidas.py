from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Medida, Opcion, OpcionMedida
from shared.dependencies import RoleChecker, SyncDbSessionDep
from shared.enums import RolesEnum
from shared.schemas import OpcionMedidaCreate, OpcionMedidaOut
from shared.utils import get_example

router = APIRouter(prefix="/opciones_medidas", tags=["Opciones Medidas"])


@router.get(
    "/",
    response_model=list[OpcionMedidaOut],
    summary="Obtener todas las opciones de medidas",
)
def read_opciones_medidas(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
): 
    """
    Devuelve una lista con todas las opciones de medidas.

    Requiere ser usuario de SMA u Organismo Sectorial para acceder a este recurso.
    """  
    opciones_medidas = db.query(OpcionMedida).join(Medida).join(Opcion).all()
    return opciones_medidas


@router.post(
    "/",
    summary="Añade una opcion de medida",
    status_code=201,
)
def add_opcion_medida(
    db: SyncDbSessionDep,
    opcion_medida: OpcionMedidaCreate = Body(
        openapi_examples={
            "default": get_example("opcion_medida_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Agrega una opción de medida a la base de datos.
    
    Argumentos:
    - id de la opción (int)
    - id de la medida (int)

    Devuelve mensaje de confirmación con el recurso creado.

    Requiere ser usuario de SMA para acceder a este recurso.
    """
    opcion = (
        db.query(Opcion).filter(Opcion.id_opcion == opcion_medida.id_opcion).first()
    )
    if not opcion:
        raise HTTPException(status_code=404, detail="Opcion no existe")
    medida = (
        db.query(Medida).filter(Medida.id_medida == opcion_medida.id_medida).first()
    )
    if not medida:
        raise HTTPException(status_code=404, detail="Medida no existe")
    if (
        db.query(OpcionMedida)
        .filter(
            OpcionMedida.id_opcion == opcion_medida.id_opcion,
            OpcionMedida.id_medida == opcion_medida.id_medida,
        )
        .first()
    ):
        raise HTTPException(status_code=409, detail="Opcion de medida ya existe")

    opcion_medida = OpcionMedida(
        id_opcion=opcion_medida.id_opcion, id_medida=opcion_medida.id_medida
    )
    db.add(opcion_medida)
    db.commit()
    db.refresh(opcion_medida)
    opcion_medida_out = OpcionMedidaOut(
        id_opcion_medida=opcion_medida.id_opcion_medida, opcion=opcion, medida=medida
    )
    return {"message": "Se creó opcion de medida", "opcion_medida": opcion_medida_out}


@router.delete(
    "/{id_opcion_medida}",
    summary="Elimina una opcion de medida",
)
def delete_opcion_medida(
    id_opcion_medida: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA])),
):
    """
    Elimina una opcion de medida por su id.

    Requiere ser usuario de SMA para acceder a este recurso.
    """
    opcion_medida = (
        db.query(OpcionMedida)
        .filter(OpcionMedida.id_opcion_medida == id_opcion_medida)
        .first()
    )
    if opcion_medida:
        db.delete(opcion_medida)
        db.commit()
    return {"message": "Se eliminó opcion de medida"}
