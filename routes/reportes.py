from io import BytesIO
from operator import and_, or_
from typing import Annotated
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from db.models import Medida, MedidaResponse, MedioVerificacion, MedioVerificacionResponse, OrganismoSectorial, OrganismoSectorialResponse, OrganismoSectorialUsuario, PlanResponse, ReporteMedidaResponse, ReporteResponse, ResultadoResponse, Usuario
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import MedioVerificacionOut, ReporteCreate, ReporteMedidaCreate, ReporteOut, ResultadoCreate, UsuarioOut
from shared.utils import get_example, get_local_now_datetime

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get(
    "/",
    # response_model=list[ReporteResponse],
    summary="Obtener todos los reportes",
    response_model_exclude_none=True,
)
async def read_reports(
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todos los reportes.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.

    En caso de ser un organismo sectorial, solo podra acceder a los reportes que le corresponden emitir.
    """
    if user.organismo_sectorial:
        reportes = (
            db.query(ReporteResponse)
            .filter(
                ReporteResponse.eliminado_por == None,
                ReporteResponse.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial,
            )
            .all()
        )
    else:
        reportes = db.query(ReporteResponse).filter(ReporteResponse.eliminado_por == None).all()
    return reportes

@router.get(
    "/{id_reporte}",
    response_model=ReporteResponse,
    summary="Obtener un reporte por ID",
    response_model_exclude_none=True,
)
async def read_report_by_id(
    id_reporte: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un reporte por ID.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.

    En caso de ser un organismo sectorial, solo podra acceder a los reportes que le corresponden emitir.
    """
    if user.organismo_sectorial:
        reporte = (
            db.query(ReporteResponse)
            .filter(
                ReporteResponse.eliminado_por == None,
                ReporteResponse.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial,
                ReporteResponse.id_reporte == id_reporte,
            )
            .first()
        )
    else:
        reporte = db.query(ReporteResponse).filter(ReporteResponse.eliminado_por == None, ReporteResponse.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte

@router.get(
    "/{id_reporte}/medidas",
    summary="Obtener las medidas de un reporte",
    response_model_exclude_none=True,
)
async def read_report_measures(
    id_reporte: int,
    db: SyncDbSessionDep,
    user: Annotated[UsuarioOut, Depends(get_user_from_token_data)],
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN, RolesEnum.FISCALIZADOR, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve las medidas de un reporte por ID.

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.

    En caso de ser un organismo sectorial, solo podra acceder a los reportes que le corresponden emitir.
    """    
    results = (
        db.query(ReporteMedidaResponse, ResultadoResponse, MedidaResponse)
        .outerjoin(ResultadoResponse, and_(
                    ResultadoResponse.id_reporte_medida == ReporteMedidaResponse.id_reporte_medida,
                    ResultadoResponse.eliminado_por == None
                ))
        .join(MedidaResponse, ReporteMedidaResponse.id_medida == MedidaResponse.id_medida)
        .filter(
            ReporteMedidaResponse.eliminado_por == None,
            ReporteMedidaResponse.id_reporte == id_reporte,
        )
        .all()
    )
    medidas = []
    for reporte_medida, resultado, medida in results:
        medidas.append({
            "id_reporte_medida": reporte_medida.id_reporte_medida,
            "medida": {
                "id_medida": medida.id_medida,
                "nombre_corto": medida.nombre_corto,
                "indicador": medida.indicador,
                "formula_calculo": medida.formula_calculo,
            },
            "resultado": {
                "id_reporte_medida": resultado.id_reporte_medida,
                "texto": resultado.texto,
                "numerico": resultado.numerico,
                "si_no": resultado.si_no,
                "id_opcion": resultado.id_opcion,
                "fecha_creacion": resultado.fecha_creacion,
                "creado_por": resultado.creado_por,
                "fecha_actualizacion": resultado.fecha_actualizacion,
                "actualizado_por": resultado.actualizado_por,
                "fecha_eliminacion": resultado.fecha_eliminacion,
                "eliminado_por": resultado.eliminado_por,
            } if resultado else None,
            "fecha_creacion": medida.fecha_creacion,
            "creado_por": medida.creado_por,
        })
    return medidas

@router.post(
    "/", 
    summary="Añade un reporte", 
    status_code=201,
)
def add_reporte(
    db: SyncDbSessionDep,
    archivo: UploadFile = File(...),
    id_plan: int = Form(..., gt=0),
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ORGANISMO_SECTORIAL])),

):
    if not db.query(PlanResponse).filter(PlanResponse.id_plan == id_plan, PlanResponse.eliminado_por == None).first():
        raise HTTPException(status_code=401, detail="El plan no existe")
    
    medidas = (
        db.query(MedidaResponse)
        .outerjoin(
            ReporteMedidaResponse,
            and_(
                ReporteMedidaResponse.id_medida == MedidaResponse.id_medida,
                ReporteMedidaResponse.eliminado_por == None
            )
        )
        .filter(
            MedidaResponse.id_plan == id_plan,
            MedidaResponse.eliminado_por == None,
            MedidaResponse.id_organismo_sectorial == user.organismo_sectorial.id_organismo_sectorial
        )
        .all()
    )
    if not medidas:
        raise HTTPException(status_code=401, detail="No existen medidas para este plan o ya han sido reportadas")
    
    try:
        reporte = ReporteResponse(
            fecha_creacion=get_local_now_datetime(),
            creado_por=user.email,
            id_organismo_sectorial=user.organismo_sectorial.id_organismo_sectorial,
            id_plan=id_plan,
        )
        db.add(reporte)
        db.flush()

        for medida in medidas:
            reporte_medida = ReporteMedidaResponse(
                id_reporte=reporte.id_reporte,
                id_medida=medida.id_medida,
                fecha_creacion=get_local_now_datetime(),
                creado_por=user.email,
            )
            db.add(reporte_medida)
            db.flush()

        medio_verificacion = MedioVerificacionResponse(
            id_reporte=reporte.id_reporte, 
            nombre_archivo=archivo.filename, 
            archivo=archivo.file.read(), 
            tamano=archivo.size, 
            fecha_creacion=get_local_now_datetime(),
            creado_por=user.email,
        )
        db.add(medio_verificacion)
        db.commit()

        db.refresh(reporte)
        db.refresh(medio_verificacion)
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el reporte")

    
    return {
        "message": "Se ha creado el reporte", 
        "reporte": {
            "id_reporte": reporte.id_reporte,
            "fecha_creacion": reporte.fecha_creacion,
            "creado_por": reporte.creado_por,
        }, 
        "medio_verificacion": {
            "id_reporte": medio_verificacion.id_reporte,
            "nombre_archivo": medio_verificacion.nombre_archivo,
            "tamano": medio_verificacion.tamano,
        }
    }

@router.post(
    "/medidas/{id_reporte_medida}/resultados", 
    summary="Añade un resultado a una medida",
    status_code=201,
)
def add_resultado(
    db: SyncDbSessionDep,
    id_reporte_medida: int,
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    reporte_medida: ResultadoCreate = Body(
        ...,
        title="Reporte Medida",
        description="Lista de medidas a reportar con su resultado",
        openapi_examples={
            "default": get_example("resultado_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ORGANISMO_SECTORIAL])),
):
    if not (
        db.query(ReporteMedidaResponse)
        .filter(
            ReporteMedidaResponse.id_reporte_medida == id_reporte_medida, 
            ReporteMedidaResponse.eliminado_por == None,
        )
        .first()
    ):
        raise HTTPException(status_code=401, detail="No existe reporte de medida con ese id")
    
    if db.query(ResultadoResponse).filter(ResultadoResponse.id_reporte_medida == id_reporte_medida).first():
        raise HTTPException(status_code=401, detail="Ya existe un resultado para este reporte de medida")

    if reporte_medida.texto is None and reporte_medida.numerico is None and reporte_medida.si_no is None and reporte_medida.id_opcion is None:
        raise HTTPException(status_code=401, detail="Debe ingresar al menos un resultado")
    
    data = ResultadoResponse(
        id_reporte_medida=id_reporte_medida,
        texto=reporte_medida.texto,
        numerico=reporte_medida.numerico,
        si_no=reporte_medida.si_no,
        id_opcion=reporte_medida.id_opcion,
        fecha_creacion=get_local_now_datetime(),
        creado_por=user.email,
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    
    return {
        "message": "Se ha creado el resultado", 
        "resultado": {
            "id_reporte_medida": data.id_reporte_medida,
            "texto": data.texto,
            "numerico": data.numerico,
            "si_no": data.si_no,
            "id_opcion": data.id_opcion,
            "fecha_creacion": data.fecha_creacion,
            "creado_por": data.creado_por,
            "fecha_actualizacion": data.fecha_actualizacion,
            "actualizado_por": data.actualizado_por,
            "fecha_eliminacion": data.fecha_eliminacion,
            "eliminado_por": data.eliminado_por,
        }
    }

@router.put(
    "/medidas/{id_reporte_medida}/resultados", 
    summary="Modifica el resultado de una medida",
)
def update_resultado(
    db: SyncDbSessionDep,
    id_reporte_medida: int,
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    reporte_medida: ResultadoCreate = Body(
        ...,
        title="Reporte Medida",
        description="Lista de medidas a reportar con su resultado",
        openapi_examples={
            "default": get_example("resultado_post"),
        }
    ),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ORGANISMO_SECTORIAL])),
):
    reporte = (
        db.query(ReporteMedidaResponse)
        .filter(
            ReporteMedidaResponse.id_reporte_medida == id_reporte_medida, 
            ReporteMedidaResponse.eliminado_por == None,
        )
        .first()
    )
    if not reporte:
        raise HTTPException(status_code=401, detail="No existe reporte de medida con ese id")
    
    resultado = (
        db.query(ResultadoResponse)
        .filter(
            ResultadoResponse.id_reporte_medida == id_reporte_medida,
            ResultadoResponse.eliminado_por == None,
        )
        .first()
    )
    if not resultado:
        raise HTTPException(status_code=401, detail="No existe un resultado para este reporte de medida")


    if reporte_medida.texto is None and reporte_medida.numerico is None and reporte_medida.si_no is None and reporte_medida.id_opcion is None:
        raise HTTPException(status_code=401, detail="Debe ingresar al menos un resultado")
    
    resultado.texto = reporte_medida.texto
    resultado.numerico = reporte_medida.numerico
    resultado.si_no = reporte_medida.si_no
    resultado.id_opcion = reporte_medida.id_opcion
    resultado.fecha_actualizacion = get_local_now_datetime()
    resultado.actualizado_por = user.email
    db.commit()
    
    return {
        "message": "Se ha actualizado el resultado", 
        "resultado": {
            "id_reporte_medida": resultado.id_reporte_medida,
            "texto": resultado.texto,
            "numerico": resultado.numerico,
            "si_no": resultado.si_no,
            "id_opcion": resultado.id_opcion,
            "fecha_creacion": resultado.fecha_creacion,
            "creado_por": resultado.creado_por,
            "fecha_actualizacion": resultado.fecha_actualizacion,
            "actualizado_por": resultado.actualizado_por,
            "fecha_eliminacion": resultado.fecha_eliminacion,
            "eliminado_por": resultado.eliminado_por,
        }
    }

@router.delete(
    "/medidas/{id_reporte_medida}/resultados", 
    summary="Elimina el resultado de una medida",
)
def delete_resultado(
    db: SyncDbSessionDep,
    id_reporte_medida: int,
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ORGANISMO_SECTORIAL, RolesEnum.ADMIN])),
):
    reporte = (
        db.query(ReporteMedidaResponse)
        .filter(
            ReporteMedidaResponse.id_reporte_medida == id_reporte_medida, 
            ReporteMedidaResponse.eliminado_por == None,
        )
        .first()
    )
    if not reporte:
        raise HTTPException(status_code=401, detail="No existe reporte de medida con ese id")
    
    resultado = (
        db.query(ResultadoResponse)
        .filter(
            ResultadoResponse.id_reporte_medida == id_reporte_medida,
            ResultadoResponse.eliminado_por == None,
        )
        .first()
    )
    if resultado:
        resultado.fecha_eliminacion = get_local_now_datetime()
        resultado.eliminado_por = user.email
        db.commit()
    return {"message": "Se eliminó resultado"}


@router.delete(
    "/{id_reporte}",
    summary="Eliminar un reporte",
)
def delete_reporte(
    id_reporte: int,
    db: SyncDbSessionDep,
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ADMIN])),
):
    '''
    Elimina un reporte por su id.
    
    Para acceder a este recurso, el usuario debe contar con el rol Administrador.
    '''
    reporte = db.query(ReporteResponse).filter(ReporteResponse.id_reporte == id_reporte, ReporteResponse.eliminado_por == None).first()
    if reporte:
        reporte_medidas = db.query(ReporteMedidaResponse).filter(ReporteMedidaResponse.id_reporte == id_reporte, ReporteMedidaResponse.eliminado_por == None).all()
        for reporte_medida in reporte_medidas:
            resultado = db.query(ResultadoResponse).filter(ResultadoResponse.id_reporte_medida == reporte_medida.id_reporte_medida, ResultadoResponse.eliminado_por == None).first()
            if resultado:
                resultado.fecha_eliminacion = get_local_now_datetime()
                resultado.eliminado_por = user.email
                db.flush()
            reporte_medida.fecha_eliminacion = get_local_now_datetime()
            reporte_medida.eliminado_por = user.email
            db.flush()
        
        reporte.fecha_eliminacion = get_local_now_datetime()
        reporte.eliminado_por = user.email
        db.flush()

        medio_verificacion = db.query(MedioVerificacionResponse).filter(MedioVerificacionResponse.id_reporte == id_reporte, MedioVerificacionResponse.eliminado_por == None).first()
        if medio_verificacion:
            medio_verificacion.fecha_eliminacion = get_local_now_datetime()
            medio_verificacion.eliminado_por = user.email
            db.flush()

        db.commit()
    return {"message": "Se ha eliminado el reporte"}

@router.get(
    "/{id_reporte}/medio_verificacion",
    summary="Descargar archivo del medio de verificación",
)
async def download_verification_file(
    id_reporte: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.FISCALIZADOR, RolesEnum.ADMIN, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Descarga el archivo asociado al medio de verificación de un reporte.

    Argumentos:
    - id del reporte (int)

    Para acceder a este recurso, el usuario debe contar con alguno de los siguientes roles: Administrador, Fiscalizador u Organismo Sectorial.
    """
    medio_verificacion = db.query(MedioVerificacion).filter(MedioVerificacion.id_reporte == id_reporte).first()

    if not medio_verificacion:
        raise HTTPException(status_code=404, detail="No existe medio de verificación para este reporte")

    return StreamingResponse(
        BytesIO(medio_verificacion.archivo),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={medio_verificacion.nombre_archivo}"},
    )