from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Medida, MedidaResponse, Opcion, OpcionResponse, OpcionMedida, OpcionMedidaResponse, OrganismoSectorial
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import OpcionMedidaCreate, OpcionMedidaOut, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

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
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las opciones de medidas.
    Si el rol es organismo sectorial, devuelve lista asociada a medidas que le correspondan a ese organismo sectorial.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador, Organismo Sectorial.
    """
    if user.rol.rol == RolesEnum.ORGANISMO_SECTORIAL:
        opciones_medidas = (
            db.query(OpcionMedidaResponse)
            .join(Medida, Medida.id_medida == OpcionMedidaResponse.id_medida)
            .filter(
                OpcionResponse.eliminado_por == None,
                MedidaResponse.eliminado_por == None,
                OpcionMedidaResponse.eliminado_por == None,
                MedidaResponse.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
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
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
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
        db.query(OpcionResponse).filter(
            OpcionResponse.id_opcion == opcion_medida.id_opcion,
            OpcionResponse.eliminado_por == None).first()
    )
    if not opcion:
        raise HTTPException(status_code=404, detail="Opcion no existe")
    medida = (
        db.query(Medida).filter(
            MedidaResponse.id_medida == opcion_medida.id_medida,
            MedidaResponse.eliminado_por == None).first()
    )
    if not medida:
        raise HTTPException(status_code=404, detail="Medida no existe")
    
    if medida.tipo_dato.tipo_dato != "Selección":
        raise HTTPException(status_code=400, detail="Solo se pueden registrar opciones para medidas con tipo de dato 'Selección'")

    if (
        db.query(OpcionMedidaResponse)
        .filter(
            OpcionMedidaResponse.id_opcion == opcion_medida.id_opcion,
            OpcionMedidaResponse.id_medida == opcion_medida.id_medida,
            OpcionMedidaResponse.eliminado_por == None,
        )
        .first()
    ):
        raise HTTPException(status_code=409, detail="Opcion de medida ya existe")

    opcion_medida = OpcionMedidaResponse(
        id_opcion=opcion_medida.id_opcion, 
        id_medida=opcion_medida.id_medida, 
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email
    )
    db.add(opcion_medida)
    db.commit()
    db.refresh(opcion_medida)
#    opcion_medida_out = OpcionMedidaOut(id_opcion_medida=opcion_medida.id_opcion_medida, opcion=opcion, medida=medida)
    return {"message": "Se agregeó la opcion de medida", "opcion_medida": opcion_medida}


@router.delete(
    "/{id_opcion_medida}",
    summary="Elimina una opcion de medida",
)
def delete_opcion_medida(
    id_opcion_medida: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una opcion de medida por su id.

    Argumentos:
    - id opcion medida (int)

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
1    """
    opcion_medida = (
        db.query(OpcionMedidaResponse)
        .filter(OpcionMedidaResponse.id_opcion_medida == id_opcion_medida, OpcionMedidaResponse.eliminado_por==None)
        .first()
    )
    if opcion_medida:
        opcion_medida.eliminado_por = user.email
        opcion_medida.fecha_eliminacion = get_local_now_datetime()
        db.commit()
    return {"message": "Se eliminó opcion de medida"}
