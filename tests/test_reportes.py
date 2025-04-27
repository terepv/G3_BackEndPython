import io
import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
    email_fiscalizador, password_fiscalizador,
    email_organismo_sectorial, password_organismo_sectorial,
)


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestReportesEndpoints():
    async def test_admin_get_reportes_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/reportes/", headers=headers)
        assert response.status_code == 200

    async def test_fiscalizador_get_reportes_success(self, client):
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/reportes/", headers=headers)
        assert response.status_code == 200

    async def test_organismo_sectorial_get_reportes_success(self, client):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/reportes/", headers=headers)
        assert response.status_code == 200

    async def test_admin_add_reporte_fail(self, client):
        file_content = b"contenido de prueba"
        archivo = ("archivo_prueba.txt", io.BytesIO(file_content), "text/plain")

        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        response = client.post("/reportes/", headers=headers, files={"archivo": archivo}, data={"id_plan": 1},)
        assert response.status_code == 401
        assert response.json() == {'detail': 'No tiene permisos para acceder a este recurso'}

    async def test_fiscalizador_add_reporte_fail(self, client):
        file_content = b"contenido de prueba"
        archivo = ("archivo_prueba.txt", io.BytesIO(file_content), "text/plain")

        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        response = client.post("/reportes/", headers=headers, files={"archivo": archivo}, data={"id_plan": 1},)
        assert response.status_code == 401
        assert response.json() == {'detail': 'No tiene permisos para acceder a este recurso'}

    async def test_organismo_sectorial_add_reporte_success(self, client):

        created_resources = []

        def get_or_create(endpoint, payload, name_field, id_field, access_token, post_object: str = None):
            headers = {"Authorization": f"Bearer {access_token}"}
            get_response = client.get(endpoint, headers=headers)
            assert get_response.status_code == 200
            existing = next((item for item in get_response.json() if item.get(name_field) == payload[name_field]), None)
            if existing:
                return existing
            post_response = client.post(endpoint, headers=headers, json=payload)
            assert post_response.status_code in (200, 201)
            resource = post_response.json()[post_object if post_object else name_field]
            created_resources.append((endpoint, resource[id_field]))
            return resource

        file_content = b"contenido de prueba exitoso"
        archivo = ("archivo_prueba_exitoso.txt", io.BytesIO(file_content), "text/plain")

        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        try: 
            rol = get_or_create("/roles/", {
                "rol": "Organismo Sectorial",
            }, "rol", "id_rol", access_token)
            assert rol["rol"] == "Organismo Sectorial"
            assert rol["id_rol"] is not None

            usuario_organismo_sectorial = get_or_create("/usuarios/", {
                "nombre": "usuario_sectorial_test_reporte",
                "apellido": "usuario_sectorial_test_reporte",
                "email": "usuario_sectorial_test_reporte@example.com",
                "password": "usuario_sectorial_test_reporte",
                "activo": True,
                "id_rol": rol["id_rol"],
                "id_organismo_sectorial": 1,
            }, "email", "id_usuario", access_token, "usuario")
            assert usuario_organismo_sectorial["nombre"] == "usuario_sectorial_test_reporte"
            assert usuario_organismo_sectorial["id_usuario"] is not None

            headers = get_basic_auth_header("usuario_sectorial_test_reporte@example.com", "usuario_sectorial_test_reporte")
            response = client.post("/auth/token", headers=headers)
            access_token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            response = client.post("/reportes/", headers=headers, files={"archivo": archivo}, data={"id_plan": 1},)
            assert response.status_code in (200, 201)
            data = response.json()
            assert data["reporte"]["id_reporte"] is not None

            response = client.get(f"/reportes/{data['reporte']['id_reporte']}/medidas/", headers=headers)
            assert response.status_code == 200

            headers = get_basic_auth_header(email_admin, password_admin)
            response = client.post("/auth/token", headers=headers)
            access_token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            response = client.delete(f"/reportes/{data['reporte']['id_reporte']}", headers=headers)
            assert response.status_code in (200, 204)

        finally:
            headers = {"Authorization": f"Bearer {access_token}"}
            for endpoint, resource_id in reversed(created_resources):
                print(f"Deleting {endpoint}{resource_id}")
                delete_response = client.delete(f"{endpoint}{resource_id}/", headers=headers)
                print(response.status_code)
                print(response.json())
                assert delete_response.status_code in (200, 204), f"Error deleting {endpoint}{resource_id}"








       


