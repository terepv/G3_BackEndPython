from fastapi import APIRouter, Body, HTTPException
from db.models import Frecuencia, Medida, OrganismoSectorial, Plan, TipoDato, TipoMedida
from shared.dependencies import SyncDbSessionDep
from shared.schemas import MedidaCreate, MedidaOut
from shared.utils import get_example

router = APIRouter(prefix="/planes/{id_plan}/medidas", tags=["Planes - Medidas"])


@router.get(
    "/",
    response_model=list[MedidaOut],
    summary="Obtener todas las medidas de un plan",
)
def read_planes_medidas(
    id_plan: int,
    db: SyncDbSessionDep,
):
    """
    Devuelve una lista con todas las medidas asociadas a un plan.
    Argumentos: 
    - id plan (int)
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="El plan no existe")

    medidas = db.query(Medida).filter(Medida.id_plan == id_plan).all()
    return medidas


@router.post(
    "/",
    summary="Agregar una medida a un plan",
    status_code=201,
)
def add_medida(
    db: SyncDbSessionDep,
    id_plan: int,
    medida: MedidaCreate = Body(
        openapi_examples={
            "default": get_example("medida_post"),
        }
    ),
):
    """
    Agrega una medida a un plan.
    Argumentos:
    - id del plan (int)
    - nombre corto medida (str)
    - indicador de la medida (str)
    - id frecuencia de la medida (int)
    - id organismo sectorial (int)
    - id tipo de medida (int)
    - descripción medio de verificación (str)
    - id tipo de dato (int)
    - cron (str)
    - reporte unico (bool)

    Devuelve mensaje de confirmación con el recurso creado.
    """
    data = Medida(
        nombre_corto=medida.nombre_corto,
        indicador=medida.indicador,
        formula_calculo=medida.formula_calculo,
        id_frecuencia=medida.id_frecuencia,
        id_organismo_sectorial=medida.id_organismo_sectorial,
        id_tipo_medida=medida.id_tipo_medida,
        id_plan=id_plan,
        desc_medio_de_verificacion=medida.desc_medio_de_verificacion,
        id_tipo_dato=medida.id_tipo_dato,
        cron=medida.cron,
        reporte_unico=medida.reporte_unico,
    )

    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    if db.query(Medida).filter(Medida.nombre_corto.ilike(data.nombre_corto)).first():
        raise HTTPException(status_code=409, detail="Medida ya existe")
    if (
        not db.query(Frecuencia)
        .filter(Frecuencia.id_frecuencia == data.id_frecuencia)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Frecuencia no existe")
    if (
        not db.query(OrganismoSectorial)
        .filter(
            OrganismoSectorial.id_organismo_sectorial == data.id_organismo_sectorial
        )
        .first()
    ):
        raise HTTPException(status_code=404, detail="Organismo sectorial no existe")
    if (
        not db.query(TipoMedida)
        .filter(TipoMedida.id_tipo_medida == data.id_tipo_medida)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de medida no existe")
    if (
        not db.query(TipoDato)
        .filter(TipoDato.id_tipo_dato == data.id_tipo_dato)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Tipo de dato no existe")

    db.add(data)
    db.commit()
    db.refresh(data)
    medida_out = MedidaOut(**data.__dict__)
    return {"message": "Se creó medida", "medida": medida_out}


@router.put(
    "/{id_medida}",
    summary="Actualizar una medida de un plan",
)
def update_medida(
    db: SyncDbSessionDep,
    id_plan: int,
    id_medida: int,
    medida: MedidaCreate = Body(
        openapi_examples={
            "default": get_example("medida_post"),
        }
    ),
):
    """
    Actualiza una medida de un plan.
    Argumentos:
    - id del plan (int) 
    - id de medida (int)
    - nombre corto medida (str)
    - indicador de la medida (str)
    - id frecuencia de la medida (int)
    - id organismo sectorial (int)
    - id tipo de medida (int)
    - descripción medio de verificación (str)
    - id tipo de dato (int)
    - cron (str)
    - reporte unico (bool)

    Devuelve mensaje de confirmación con el recurso actualizado.
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")

    medida_db = db.query(Medida).filter(Medida.id_medida == id_medida).first()
    if not medida_db:
        raise HTTPException(status_code=404, detail="Medida no existe")

    if not db.query(Medida).filter(Medida.id_medida == id_medida).first():
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
    medida_db.cron = medida.cron
    medida_db.reporte_unico = medida.reporte_unico

    db.commit()
    db.refresh(medida_db)

    medida_out = MedidaOut(**medida_db.__dict__)

    return {"message": "Se actualizó la medida", "medida": medida_out}


@router.delete(
    "/{id_medida}",
    summary="Elimina una medida de un plan por su id",
)
def delete_medida(
    id_plan: int,
    id_medida: int,
    db: SyncDbSessionDep,
):
    """
    Elimina una medida de un plan por su id.
    Argumentos:
    - id plan (int)
    - id medida (int)

    Devuelve mensaje de confirmación.
    """
    if not db.query(Plan).filter(Plan.id_plan == id_plan).first():
        raise HTTPException(status_code=404, detail="Plan no existe")
    medida = db.query(Medida).filter(Medida.id_medida == id_medida).first()
    if medida:
        db.delete(medida)
        db.commit()
    return {"message": "Se eliminó medida"}
