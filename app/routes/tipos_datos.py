from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from app.db.models import TipoDatoResponse
from app.shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from app.shared.enums import RolesEnum
from app.shared.utils import get_example, get_local_now_datetime
from app.shared.schemas import TipoDatoCreate, UsuarioOut

router = APIRouter(prefix="/tipos_datos", tags=["Tipos de Datos"])


@router.get(
    "/",
    response_model=list[TipoDatoResponse],
    response_model_exclude_none=True,
    summary="Obtener todos los tipos de datos",
)
def read_tipo_datos(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todos los tipos de datos.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    tipo_datos = db.query(TipoDatoResponse).filter(TipoDatoResponse.eliminado_por == None).all()
    return tipo_datos

####
@router.get(
    "/tipo_dato/{id_tipo_dato}",
    response_model_exclude_none=True,
    response_model=TipoDatoResponse,
    summary="Obtener un tipo de dato por su id",
)
def read_tipo_datos(
    id_tipo_dato: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un tipo de dato por su id.

    Argumentos:
    - id tipo dato (int)

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    tipo_dato = db.query(TipoDatoResponse).filter(TipoDatoResponse.id_tipo_dato == id_tipo_dato, TipoDatoResponse.eliminado_por == None).first()
    if not tipo_dato:
        raise HTTPException(status_code=404, detail="No existe un tipo de dato con ese id")
    return tipo_dato

@router.post(
    "/", 
    summary="Añade un tipo de dato", 
    status_code=201,
    response_model_exclude_none=True,
)
def add_tipo_dato(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    tipo_dato: TipoDatoCreate = Body(
        openapi_examples={
            "default": get_example("tipo_dato_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega un tipo de dato.
    
    Argumentos:
    - tipo de dato (str)
    - id_tipo_dato (int)

    Devuelve un mensaje de confirmación con el recurso creado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    if db.query(TipoDatoResponse).filter(TipoDatoResponse.tipo_dato.ilike(tipo_dato.tipo_dato), TipoDatoResponse.eliminado_por == None).first():
        raise HTTPException(status_code=409, detail="Tipo de dato ya existe")

    data = TipoDatoResponse(
        tipo_dato=tipo_dato.tipo_dato,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return {"message": "Se creó un tipo de dato", "Tipo de dato": data}

@router.put(
    "/{id_tipo_dato}", 
    summary="Actualiza un tipo de dato por su id", 
    response_model_exclude_none=True,
)
def add_tipo_dato(
    id_tipo_dato: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    tipo_dato: TipoDatoCreate = Body(
        openapi_examples={
            "default": get_example("tipo_dato_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza un tipo de dato por su id.
    
    Argumentos:
    - nombre del tipo de dato (str)
    - id_tipo_dato (int)

    Devuelve un mensaje de confirmación con el recurso creado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """

    data = db.query(TipoDatoResponse).filter(TipoDatoResponse.id_tipo_dato == id_tipo_dato, TipoDatoResponse.eliminado_por == None).first()
    if not data:
        raise HTTPException(status_code=404, detail="No existe un tipo de dato con ese id")

    if db.query(TipoDatoResponse).filter(
        TipoDatoResponse.tipo_dato.ilike(tipo_dato.tipo_dato), 
        TipoDatoResponse.id_tipo_dato != id_tipo_dato, 
        TipoDatoResponse.eliminado_por == None
    ).first():
        raise HTTPException(status_code=409, detail="Tipo de dato ya existe")

    data.fecha_actualizacion = get_local_now_datetime()
    data.tipo_dato = tipo_dato.tipo_dato
    data.actualizado_por = user.email
    db.commit()

    return {"message": "Se actualizó tipo de dato", "Tipo de dato": data}

@router.delete(
    "/{id_tipo_dato}",
    summary="Elimina un tipo de dato por su id",
    status_code=200,
)
def delete_tipo_dato(
    id_tipo_dato: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina un tipo de dato por su id.

    Argumentos:
    - id tipo dato (int)

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    tipo_dato = db.query(TipoDatoResponse).filter(TipoDatoResponse.id_tipo_dato == id_tipo_dato, TipoDatoResponse.eliminado_por == None).first()
    if tipo_dato:
        tipo_dato.fecha_eliminacion = get_local_now_datetime()
        tipo_dato.eliminado_por = user.email
        db.commit()

    return {"message": "Se eliminó un tipo de dato"}