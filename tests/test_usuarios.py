import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
)


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestUsuariosEndpoints():
    async def test_admin_get_usuarios_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/usuarios/", headers=headers)
        assert response.status_code == 200

    async def test_crud_usuarios_success(self, client):
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
        
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        
        try: 
            rol = get_or_create("/roles/", {
                "rol": "Administrador",
            }, "rol", "id_rol", access_token)
            assert rol["rol"] == "Administrador"
            assert rol["id_rol"] is not None

            usuario_admin = get_or_create("/usuarios/", {
                "nombre": "usuario_admin_test_usuario",
                "apellido": "usuario_admin_test",
                "email": "usuario_admin_test@example.com",
                "password": "usuario_admin_test",
                "activo": True,
                "id_rol": rol["id_rol"],
                "id_organismo_sectorial": None,
            }, "email", "id_usuario", access_token, "usuario")
            assert usuario_admin["nombre"] == "usuario_admin_test_usuario"
            assert usuario_admin["id_usuario"] is not None

        finally:
            headers = {"Authorization": f"Bearer {access_token}"}
            for endpoint, resource_id in reversed(created_resources):
                # print(f"Deleting {endpoint}{resource_id}")
                delete_response = client.delete(f"{endpoint}{resource_id}/", headers=headers)
                assert delete_response.status_code in (200, 204), f"Error deleting {endpoint}{resource_id}"