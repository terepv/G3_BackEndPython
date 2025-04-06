from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from db.models import Frecuencia, Medida, MedidaResponse, OrganismoSectorial, Plan, PlanResponse, TipoDato, TipoMedida
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import MedidaCreate, MedidaOut, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/planes/{id_plan}/medidas", tags=["Planes - Medidas"])


@router.get(
    "/",
    response_model=list[MedidaResponse],
    response_model_exclude_none=True,
    summary="Obtener todas las medidas de un plan",
)
def read_planes_medidas(
    id_plan: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todas las medidas de un plan.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.

    En caso de ser un organismo sectorial, solo podra acceder a los planes que le corresponden emitir un reporte.
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="El plan no existe")

    if user.rol.rol == RolesEnum.ORGANISMO_SECTORIAL:
        medidas = (
            db.query(MedidaResponse)
            .join(PlanResponse, PlanResponse.id_plan == Medida.id_plan)
            .filter(
                PlanResponse.eliminado_por == None,
                Medida.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
            )
            .all()
        )
    else:
        medidas = db.query(MedidaResponse).filter(MedidaResponse.id_plan == id_plan, MedidaResponse.eliminado_por == None).all()
    return medidas


@router.post(
    "/",
    summary="Agregar una medida a un plan",
    status_code=201,
    response_model_exclude_none=True,
)
def add_medida(
    db: SyncDbSessionDep,
    id_plan: int,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    medida: MedidaCreate = Body(
        openapi_examples={
            "default": get_example("medida_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Agrega una medida a un plan.
    
    Argumentos:
    - id del plan (int)
    - nombre corto de la medida (str)
    - indicador de la medida (str)
    - fórmula de cálculo (str)
    - id de la frecuencia (int)
    - id del organismo sectorial (int)
    - id del tipo de medida (int)
    - descripción del medio de verificación (str)
    - id del tipo de dato (int)
    - reporte unico (bool)
    
    Devuelve mensaje de confirmación con el recurso creado.
    
    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """

    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    if db.query(Medida).filter(Medida.nombre_corto.ilike(medida.nombre_corto)).first():
        raise HTTPException(status_code=409, detail="Medida ya existe")
    if (
        not db.query(Frecuencia)
        .filter(Frecuencia.id_frecuencia == medida.id_frecuencia)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Frecuencia no existe")
    if (
        not db.query(OrganismoSectorial)
        .filter(
            OrganismoSectorial.id_organismo_sectorial == medida.id_organismo_sectorial
        )
        .first()
    ):
        raise HTTPException(status_code=404, detail="Organismo sectorial no existe")
    if (
        not db.query(TipoMedida)
        .filter(TipoMedida.id_tipo_medida == medida.id_tipo_medida)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de medida no existe")
    if (
        not db.query(TipoDato)
        .filter(TipoDato.id_tipo_dato == medida.id_tipo_dato)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de dato no existe")

    data = MedidaResponse(
        nombre_corto=medida.nombre_corto,
        indicador=medida.indicador,
        formula_calculo=medida.formula_calculo,
        id_frecuencia=medida.id_frecuencia,
        id_organismo_sectorial=medida.id_organismo_sectorial,
        id_tipo_medida=medida.id_tipo_medida,
        id_plan=id_plan,
        desc_medio_de_verificacion=medida.desc_medio_de_verificacion,
        id_tipo_dato=medida.id_tipo_dato,
        reporte_unico=medida.reporte_unico,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message": "Se creó medida", "medida": data}


@router.put(
    "/{id_medida}",
    summary="Actualizar una medida de un plan",
    response_model_exclude_none=True,
)
def update_medida(
    db: SyncDbSessionDep,
    id_plan: int,
    id_medida: int,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    medida: MedidaCreate = Body(
        openapi_examples={
            "default": get_example("medida_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Actualiza una medida de un plan.
    
    Argumentos:
    - id del plan (int)
    - id de la medida (int)
    - nombre corto de la medida (str)
    - indicador de la medida (str)
    - fórmula de cálculo (str)
    - id de la frecuencia (int)
    - id del organismo sectorial (int)
    - id del tipo de medida (int)
    - descripción del medio de verificación (str)
    - id del tipo de dato (int)
    - reporte unico (bool)
    
    Devuelve mensaje de confirmación con el recurso actualizado.
    
    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")

    medida_db = db.query(MedidaResponse).filter(MedidaResponse.id_medida == id_medida, MedidaResponse.eliminado_por == None).first()
    if not medida_db:
        raise HTTPException(status_code=404, detail="Medida no existe")
    
    if (
        not db.query(Frecuencia)
        .filter(Frecuencia.id_frecuencia == medida.id_frecuencia)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Frecuencia no existe")
    if (
        not db.query(OrganismoSectorial)
        .filter(
            OrganismoSectorial.id_organismo_sectorial == medida.id_organismo_sectorial
        )
        .first()
    ):
        raise HTTPException(status_code=404, detail="Organismo sectorial no existe")
    if (
        not db.query(TipoMedida)
        .filter(TipoMedida.id_tipo_medida == medida.id_tipo_medida)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de medida no existe")
    if (
        not db.query(TipoDato)
        .filter(TipoDato.id_tipo_dato == medida.id_tipo_dato)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de dato no existe")

    medida_db.nombre_corto = medida.nombre_corto
    medida_db.indicador = medida.indicador
    medida_db.formula_calculo = medida.formula_calculo
    medida_db.id_frecuencia = medida.id_frecuencia
    medida_db.id_organismo_sectorial = medida.id_organismo_sectorial
    medida_db.id_tipo_medida = medida.id_tipo_medida
    medida_db.id_plan = id_plan
    medida_db.desc_medio_de_verificacion = medida.desc_medio_de_verificacion
    medida_db.id_tipo_dato = medida.id_tipo_dato
    medida_db.reporte_unico = medida.reporte_unico
    medida_db.fecha_actualizacion = get_local_now_datetime()
    medida_db.actualizado_por = user.email

    db.commit()
    db.refresh(medida_db)

    return {"message": "Se actualizó la medida", "medida": medida_db}


@router.delete(
    "/{id_medida}",
    summary="Elimina una medida de un plan por su id",
)
def delete_medida(
    id_plan: int,
    id_medida: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    """
    Elimina una medida de un plan por su id.

    Argumentos:
    - id del plan (int)
    - id de la medida (int)

    Devuelve un mensaje de confirmación con el recurso eliminado.

    Para acceder a este recurso, el usuario debe tener el rol: Administrador.
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    
    medida = db.query(MedidaResponse).filter(MedidaResponse.id_medida == id_medida, MedidaResponse.eliminado_por == None).first()
    if medida:
        medida.fecha_eliminacion = get_local_now_datetime()
        medida.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó medida"}
