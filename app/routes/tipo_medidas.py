from fastapi import APIRouter, Body, Depends, HTTPException
from app.db.models import TipoMedida, TipoMedidaResponse
from app.shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from app.shared.enums import RolesEnum
from app.shared.schemas import TipoMedidaCreate, UsuarioOut
from app.shared.utils import get_example, get_local_now_datetime
from typing_extensions import Annotated

router = APIRouter(prefix="/tipo_medidas", tags=["Tipo Medidas"])


@router.get(
    "/",
    response_model=list[TipoMedida],
    summary="Obtener todos los tipos de medidas",
)
def read_tipo_medidas(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """Devuelve una lista con todos los tipos de medidas.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    tipo_medidas = db.query(TipoMedidaResponse).filter(TipoMedidaResponse.eliminado_por == None).all()
    return tipo_medidas


@router.get(
    "/{id_tipo_medida}",
    response_model=TipoMedida,
    summary="Obtener un tipo de medida por su id",
)
def read_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un tipo de medida por su id.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    tipo_medida = (
        db.query(TipoMedidaResponse).filter(TipoMedidaResponse.id_tipo_medida == id_tipo_medida, TipoMedidaResponse.eliminado_por == None).first()
    )
    if not tipo_medida:
        raise HTTPException(
            status_code=404, detail="No existe tipo de medida con ese id"
        )
    return tipo_medida


@router.post(
    "/",
    summary="Añade un tipo de medida",
    status_code=201,
)
def add_tipo_medida(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    tipo_medida: TipoMedidaCreate = Body(
        openapi_examples={
            "default": get_example("tipo_medida_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega un tipo de medida a la base de datos.

    Argumentos:
    - tipo_medida (str)

    Devuelve mensaje de confirmación con el recurso creado.
    
    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    nombre_tipo_medida = tipo_medida.tipo_medida

    if (
        db.query(TipoMedidaResponse)
        .filter(TipoMedidaResponse.tipo_medida.ilike(nombre_tipo_medida),
                TipoMedidaResponse.eliminado_por == None)
        .first()
    ):
        raise HTTPException(status_code=409, detail="Tipo de medida ya existe")
    
    if len(nombre_tipo_medida) < 3:
        raise HTTPException(
            status_code=400, detail="Nombre de tipo de medida muy corto"
        )
    
    if len(nombre_tipo_medida) > 100:
        raise HTTPException(
            status_code=400, detail="Nombre de tipo de medida muy largo"
        )

    data = TipoMedidaResponse(
        tipo_medida=nombre_tipo_medida,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return {"message": "Se creó tipo de medida", "Tipo de medida": data}


@router.delete(
    "/{id_tipo_medida}",
    summary="Elimina un tipo de medida",
)
def delete_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
        user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):

    """
    Elimina un tipo de medida por su id.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    tipo_medida = (
        db.query(TipoMedidaResponse).filter(TipoMedidaResponse.id_tipo_medida == id_tipo_medida, TipoMedidaResponse.eliminado_por == None).first()
    )
    if tipo_medida:
        tipo_medida.fecha_eliminacion = get_local_now_datetime()
        tipo_medida.eliminado_por = user.email
        db.commit()

    return {"message": "Se eliminó tipo de medida"}

@router.put(
    "/{id_tipo_medida}",
    summary="Actualiza un tipo de medida por su id",
    response_model_exclude_none=True,
)
def update_tipo_medida(
    id_tipo_medida: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    tipo_medida: TipoMedidaCreate = Body(
        openapi_examples={
            "default": get_example("tipo_medida_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza un tipo de medida por su id.

    Argumentos:
    - nombre del tipo de medida (str)
    - fecha de creación del tipo de medida (datetime)

    Devuelve mensaje de confirmación con el recurso actualizado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """

    data = db.query(TipoMedidaResponse).filter(TipoMedidaResponse.id_tipo_medida == id_tipo_medida, TipoMedidaResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe tipo de medida con ese id")
    if db.query(TipoMedidaResponse).filter(TipoMedidaResponse.id_tipo_medida != id_tipo_medida, TipoMedidaResponse.tipo_medida.ilike(tipo_medida.tipo_medida), TipoMedidaResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Tipo de medida ya existe")
    data.tipo_medida = tipo_medida.tipo_medida
    data.fecha_actualizacion = get_local_now_datetime()
    data.actualizado_por = user.email
    db.commit()

    return (
        {"message": "Se actualizó tipo de medida", "Tipo de medida": data}
    )