from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Medida, MedidaResponse, Opcion, OpcionResponse, OpcionMedida, OpcionMedidaResponse, OrganismoSectorial
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import OpcionMedidaCreate, OpcionMedidaOut, UsuarioOut
from shared.utils import get_example

router = APIRouter(prefix="/opciones_medidas", tags=["Opciones Medidas"])


@router.get(
    "/",
    response_model=list[OpcionMedidaOut],
    response_model_exclude_none=True,
    summary="Obtener todas las opciones de medidas",
)
def read_opciones_medidas(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Si el usuario cuenta con rol administrador, devuelve una lista con todas las opciones de medidas.
    Si el usuario cuenta con rol de organismo sectorial, devuelve lista de opciones de medidas que le correspondan a ese organismo sectorial.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Organismo Sectorial.
    """
    if user.rol.rol == RolesEnum.ORGANISMO_SECTORIAL:
        opciones_medidas = (
            db.query(OpcionMedidaResponse)
            .join(OpcionResponse, OpcionResponse.id_opcion == OpcionMedidaResponse.id_opcion)
            .join(MedidaResponse, MedidaResponse.id_medida == OpcionMedidaResponse.id_medida)
            .filter(
                OpcionResponse.eliminado_por == None,
                MedidaResponse.eliminado_por == None,
                OpcionMedidaResponse.eliminado_por == None,
                MedidaResponse.organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
            ).all()
        )
    else:
        opciones_medidas = db.query(
            OpcionMedidaResponse).filter(
                OpcionMedidaResponse.eliminado_por == None
            ).all()
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
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega una opción de medida a la base de datos.
    
    Argumentos:
    - id de la opción (int)
    - id de la medida (int)

    Devuelve mensaje de confirmación con el recurso creado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
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
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una opcion de medida por su id.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
1    """
    opcion_medida = (
        db.query(OpcionMedida)
        .filter(OpcionMedida.id_opcion_medida == id_opcion_medida)
        .first()
    )
    if opcion_medida:
        db.delete(opcion_medida)
        db.commit()
    return {"message": "Se eliminó opcion de medida"}
