from base64 import b64encode
from datetime import datetime
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.database import SessionDepAsync
from app.db.models import ComunaResponse, OrganismoSectorialResponse, Rol, TipoMedida, TipoMedidaResponse, UsuarioResponse, RegionResponse
from app.shared.utils import get_password_hash

creado_por = "hpinilla@gmail.com"
email_admin = "admin@example.com"
password_admin = "adminpassword"
email_fiscalizador = "fiscalizador@example.com"
password_fiscalizador = "fiscalizadorpassword"
email_organismo_sectorial = "organismo_sectorial@example.com"
password_organismo_sectorial = "organismo_sectorial_password"
organismo_sectorial_name = "OS Test"

def get_basic_auth_header(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

@pytest_asyncio.fixture(scope="function")
def client():
    from app.main import app
    from fastapi.testclient import TestClient
    app.state.limiter.reset()
    client = TestClient(app)
    yield client

@pytest_asyncio.fixture(scope="session")
async def create_and_delete_test_users():
    #setup
    async with SessionDepAsync() as db:
        async def get_rol_by_name(rol_name) -> Rol:
            result = await db.execute(select(Rol).filter(Rol.rol == rol_name))
            rol = result.scalars().first()
            if not rol:
                raise Exception(f"Rol '{rol_name}' no encontrado")
            return rol
        
        async def create_organismo_sectorial(organismo_sectorial) -> OrganismoSectorialResponse:
            new_organismo_sectorial = OrganismoSectorialResponse(
                organismo_sectorial=organismo_sectorial,
                fecha_creacion=datetime.now(),
                creado_por=creado_por
            )
            db.add(new_organismo_sectorial)
            await db.commit()
            await db.refresh(new_organismo_sectorial)
            return new_organismo_sectorial
        
        async def create_user(email: str, password: str, rol: Rol, organismo_sectorial: OrganismoSectorialResponse = None):
            result = await db.execute(select(UsuarioResponse).filter(UsuarioResponse.email == email))
            user = result.scalars().first()
            if not user:
                new_user = UsuarioResponse(
                    nombre=email.split("@")[0],
                    apellido="Test",
                    email=email,
                    password=get_password_hash(password),
                    id_rol=rol.id_rol,
                    id_organismo_sectorial=organismo_sectorial.id_organismo_sectorial if organismo_sectorial else None,
                    activo=True,
                    fecha_creacion=datetime.now(),
                    creado_por=creado_por
                )
                db.add(new_user)
                await db.commit()

        rol_admin = await get_rol_by_name("Administrador")
        rol_fiscalizador = await get_rol_by_name("Fiscalizador")
        rol_organismo_sectorial = await get_rol_by_name("Organismo Sectorial")
        
        await create_user(email_admin, password_admin, rol_admin)
        await create_user(email_fiscalizador, password_fiscalizador, rol_fiscalizador)
        new_organismo_sectorial = await create_organismo_sectorial(organismo_sectorial_name)
        await create_user(email_organismo_sectorial, password_organismo_sectorial, rol_organismo_sectorial, new_organismo_sectorial)

    yield 
    # Teardown 
    async with SessionDepAsync() as db:
        result = await db.execute(select(UsuarioResponse).filter(UsuarioResponse.email == email_admin))
        user = result.scalars().first()
        if user:
            await db.delete(user)

        result = await db.execute(select(UsuarioResponse).filter(UsuarioResponse.email == email_fiscalizador))
        user = result.scalars().first()
        if user:
            await db.delete(user)

        result = await db.execute(select(UsuarioResponse).filter(UsuarioResponse.email == email_organismo_sectorial))
        user = result.scalars().first()
        if user:
            await db.delete(user)

        result = await db.execute(select(OrganismoSectorialResponse).filter(OrganismoSectorialResponse.organismo_sectorial == organismo_sectorial_name))
        organismo_sectorial = result.scalars().first()
        if organismo_sectorial:
            await db.delete(organismo_sectorial)

        await db.commit()


tipo_medida_name = "Tipo Medida Test"

@pytest_asyncio.fixture(scope="class")
async def delete_tipo_medida_if_exists():
    yield
    async with SessionDepAsync() as db:
        result = await db.execute(select(TipoMedida).filter(TipoMedida.tipo_medida == tipo_medida_name))
        tipo_medida = result.scalars().first()
        if tipo_medida:
            await db.delete(tipo_medida)
            await db.commit()

@pytest_asyncio.fixture(scope="function")
async def tipo_medida_test():
    async with SessionDepAsync() as db:
        result = await db.execute(select(TipoMedida).filter(TipoMedida.tipo_medida == tipo_medida_name))
        tipo_medida = result.scalars().first()
        if not tipo_medida:
            tipo_medida = TipoMedidaResponse(
            tipo_medida=tipo_medida_name,
            fecha_creacion=datetime.now(),
            creado_por=creado_por,
            )
            db.add(tipo_medida)
            await db.commit()
            await db.refresh(tipo_medida)
    yield tipo_medida

region_test_name = "Región Test"

@pytest_asyncio.fixture(scope="class")
async def delete_region_if_exists():
    yield
    async with SessionDepAsync() as db:
        result = await db.execute(select(RegionResponse).filter(RegionResponse.region == region_test_name))
        region = result.scalars().first()
        if region:
            await db.delete(region)
            await db.commit()

@pytest_asyncio.fixture(scope="function")
async def region_test():
    async with SessionDepAsync() as db:
        result = await db.execute(select(RegionResponse).filter(RegionResponse.region == region_test_name))
        region = result.scalars().first()
        if not region:
            region = RegionResponse(
                region=region_test_name,
                fecha_creacion=datetime.now(),
                creado_por=creado_por,
            )
            db.add(region)
            await db.commit()
            await db.refresh(region)
    yield region

comuna_test_name = "Comuna Test"

@pytest_asyncio.fixture(scope="class")
async def delete_comuna_if_exists():
    yield
    async with SessionDepAsync() as db:
        result = await db.execute(select(ComunaResponse).filter(ComunaResponse.comuna == comuna_test_name))
        comuna = result.scalars().first()
        if comuna:
            await db.delete(comuna)
            await db.commit()

from sqlalchemy.orm import joinedload

@pytest_asyncio.fixture(scope="function")
async def comuna_test(region_test):
    """Fixture que crea una comuna de prueba y la asocia a una región de prueba."""
    async with SessionDepAsync() as db:
        # Primero verificar si la comuna ya existe
        result = await db.execute(
            select(ComunaResponse)
            .options(joinedload(ComunaResponse.region))
            .filter(
                ComunaResponse.comuna == comuna_test_name,
                ComunaResponse.eliminado_por == None
            )
        )
        comuna = result.scalars().first()
        
        if not comuna:
            # Crear nueva comuna si no existe
            comuna = ComunaResponse(
                comuna=comuna_test_name,
                id_region=region_test.id_region,
                fecha_creacion=datetime.now(),
                creado_por=creado_por,
            )
            db.add(comuna)
            await db.commit()
            await db.refresh(comuna)
            
            # Volver a cargar la comuna con su relación
            result = await db.execute(
                select(ComunaResponse)
                .options(joinedload(ComunaResponse.region))
                .filter(ComunaResponse.id_comuna == comuna.id_comuna)
            )
            comuna = result.scalars().first()
        
    return comuna