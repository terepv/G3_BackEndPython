from io import BytesIO
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from db.models import Medida, MedioVerificacion, OrganismoSectorialUsuario, Reporte, Usuario
from shared.dependencies import RoleChecker, SyncDbSessionDep, get_user_from_token_data
from shared.enums import RolesEnum
from shared.schemas import MedioVerificacionOut, ReporteOut, UsuarioOut

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get(
    "/",
    response_model=list[ReporteOut],
    summary="Obtener todos los reportes",
)
async def read_reports(
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve una lista con todos los reportes.

    Requiere estar autenticado con rol de SMA u Organismo Sectorial para acceder a este recurso.
    """
    results = db.query(Reporte, MedioVerificacion).outerjoin(MedioVerificacion, Reporte.id_reporte == MedioVerificacion.id_reporte).all()
    reports = []
    for report, medio_verificacion in results:
        medio_verificacion_out = None
        if medio_verificacion:
            medio_verificacion_out = MedioVerificacionOut(
                id_reporte=medio_verificacion.id_reporte,
                nombre_archivo=medio_verificacion.nombre_archivo,
                tamano=medio_verificacion.tamano
            )
        reports.append(ReporteOut(
            id_reporte=report.id_reporte,
            id_medida=report.id_medida,
            id_usuario_creacion=report.id_usuario_creacion,
            usuario_creacion=report.usuario_creacion, 
            fecha_registro=report.fecha_registro,
            medio_verificacion=medio_verificacion_out
        ))
    return reports

@router.get(
    "/{id_reporte}",
    response_model=ReporteOut,
    summary="Obtener un reporte por su id",
)
def read_report(
    id_reporte: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Devuelve un reporte por su id.

    Argumentos:
    - id del reporte (int)

    Requiere estar autenticado con rol de SMA u Organismo Sectorial para acceder a este recurso.
    """
    result = db.query(Reporte, MedioVerificacion).outerjoin(MedioVerificacion, Reporte.id_reporte == MedioVerificacion.id_reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not result:
        raise HTTPException(status_code=404, detail="No existe reporte con ese id")

    reporte, medio_verificacion = result
    medio_verificacion_out = None
    if medio_verificacion:
        medio_verificacion_out = MedioVerificacionOut(
            id_reporte=medio_verificacion.id_reporte,
            nombre_archivo=medio_verificacion.nombre_archivo,
            tamano=medio_verificacion.tamano
        )

    return ReporteOut(
        id_reporte=reporte.id_reporte,
        id_medida=reporte.id_medida,
        id_usuario_creacion=reporte.id_usuario_creacion,
        usuario_creacion=reporte.usuario_creacion, 
        fecha_registro=reporte.fecha_registro,
        medio_verificacion=medio_verificacion_out
    )

@router.post(
    "/", 
    summary="Añade un reporte", 
    status_code=201,
)
def add_reporte(
    db: SyncDbSessionDep,
    id_medida: int = Form(..., description="Id de la medida a la que se le reportará"),
    archivo: UploadFile = File(...),
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.ORGANISMO_SECTORIAL])),
):
    medida = db.query(Medida).filter(Medida.id_medida == id_medida).first()
    if not medida:
        raise HTTPException(status_code=404, detail="No existe medida con ese id")
    organismo_sectorial_medida = db.query(Usuario).filter(Usuario.id_usuario == user.id_usuario).join(OrganismoSectorialUsuario).filter(OrganismoSectorialUsuario.id_organismo_sectorial == medida.id_organismo_sectorial).first()
    if not organismo_sectorial_medida:
        raise HTTPException(status_code=401, detail="El usuario no pertenece al organismo sectorial que debe reportar la medida")
    
    reporte = Reporte(id_medida=id_medida, id_usuario_creacion=user.id_usuario)
    db.add(reporte)
    db.commit()
    db.refresh(reporte)

    medio_verificacion = MedioVerificacion(id_reporte=reporte.id_reporte, archivo=archivo.file.read(), nombre_archivo=archivo.filename, tamano=archivo.size, reporte=reporte)
    db.add(medio_verificacion)
    db.commit()
    db.refresh(medio_verificacion)

    return {"message": "Se ha creado el reporte"}

@router.delete(
    "/{id_reporte}",
    summary="Eliminar un reporte",
)
def delete_reporte(
    id_reporte: int,
    db: SyncDbSessionDep,
    user: UsuarioOut | None = Depends(get_user_from_token_data),
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if reporte:
        medida = db.query(Medida).filter(Medida.id_medida == reporte.id_medida).first()
        if not medida:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No existe medida con ese id")
        organismo_sectorial_medida = db.query(Usuario).filter(Usuario.id_usuario == user.id_usuario).join(OrganismoSectorialUsuario).filter(OrganismoSectorialUsuario.id_organismo_sectorial == medida.id_organismo_sectorial).first()
        if not organismo_sectorial_medida:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El usuario no pertenece al organismo sectorial que reportó la medida")
        db.delete(reporte)
        db.commit()
    return {"message": "Se ha eliminado el reporte"}

@router.get(
    "/{id_reporte}/archivo",
    summary="Descargar archivo del medio de verificación",
)
async def download_verification_file(
    id_reporte: int,
    db: SyncDbSessionDep,
    _: bool = Depends(RoleChecker(allowed_roles=[RolesEnum.SMA, RolesEnum.ORGANISMO_SECTORIAL])),
):
    """
    Descarga el archivo asociado al medio de verificación de un reporte.

    Argumentos:
    - id del reporte (int)

    Requiere estar autenticado con rol de SMA u Organismo Sectorial para acceder a este recurso.
    """
    medio_verificacion = db.query(MedioVerificacion).filter(MedioVerificacion.id_reporte == id_reporte).first()

    if not medio_verificacion:
        raise HTTPException(status_code=404, detail="No existe medio de verificación para este reporte")

    return StreamingResponse(
        BytesIO(medio_verificacion.archivo),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={medio_verificacion.nombre_archivo}"},
    )