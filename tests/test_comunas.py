import pytest
from datetime import datetime
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, get_basic_auth_header, password_admin,
    email_fiscalizador, password_fiscalizador, email_organismo_sectorial, password_organismo_sectorial,
    creado_por, comuna_test_name, delete_comuna_if_exists, comuna_test, region_test
)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
@pytest.mark.usefixtures("delete_comuna_if_exists")
class TestComunasEndpoints():
    # ####################################################
    # GET /comunas
    # ####################################################
    async def test_admin_get_comunas_success(self, client):
        """Un usuario admin puede obtener todas las comunas."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/comunas/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_fiscalizador_get_comunas_success(self, client):
        """Un usuario fiscalizador puede obtener todas las comunas."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/comunas/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_organismo_sectorial_get_comunas_success(self, client):
        """Un usuario organismo sectorial puede obtener todas las comunas."""
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/comunas/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_comunas_unauthorized(self, client):
        """Un usuario no autenticado no puede acceder al endpoint."""
        response = client.get("/comunas/")
        assert response.status_code == 401
        assert response.json().get("detail") == "Credenciales invalidas"

    # ####################################################
    # GET /comunas/comuna/{id_comuna}
    # ####################################################
    async def test_admin_get_comuna_success(self, client, comuna_test):
        """Un usuario admin puede obtener una comuna específica."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/comunas/comuna/{comuna_test.id_comuna}", headers=headers)
        assert response.status_code == 200
        assert response.json()["comuna"] == comuna_test_name

    async def test_fiscalizador_get_comuna_success(self, client, comuna_test):
        """Un usuario fiscalizador puede obtener una comuna específica."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/comunas/comuna/{comuna_test.id_comuna}", headers=headers)
        assert response.status_code == 200
        assert response.json()["comuna"] == comuna_test_name

    async def test_get_comuna_not_found(self, client):
        """Obtener una comuna que no existe devuelve 404."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/comunas/comuna/99999", headers=headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe comuna con ese id"

    # ####################################################
    # POST /comunas
    # ####################################################
    async def test_admin_create_comuna_success(self, client, region_test):
        """Un usuario admin puede crear una comuna."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        new_comuna_name = f"Nueva Comuna {datetime.now().strftime('%Y%m%d%H%M%S')}"
        response = client.post("/comunas/", headers=headers, json={
            "comuna": new_comuna_name,
            "id_region": region_test.id_region
        })
        assert response.status_code == 201
        assert response.json()["comuna"]["comuna"] == new_comuna_name

    async def test_admin_create_comuna_invalid_region(self, client):
        """No se puede crear una comuna con una región que no existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/comunas/", headers=headers, json={
            "comuna": "Nueva Comuna",
            "id_region": 99999
        })
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe región con ese id"

    # ####################################################
    # PUT /comunas/{comuna_id}
    # ####################################################
    async def test_admin_update_comuna_success(self, client, comuna_test, region_test):
        """Un usuario admin puede actualizar una comuna."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        updated_name = f"{comuna_test_name}_updated"
        response = client.put(
            f"/comunas/{comuna_test.id_comuna}", 
            headers=headers, 
            json={
                "comuna": updated_name,
                "id_region": region_test.id_region
            },
            params={"id_comuna": comuna_test.id_comuna}
        )
        assert response.status_code == 201
        assert response.json()["comuna"]["comuna"] == updated_name

    async def test_admin_update_nonexistent_comuna_fails(self, client, region_test):
        """No se puede actualizar una comuna que no existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put(
            "/comunas/99999", 
            headers=headers, 
            json={
                "comuna": "Comuna Actualizada",
                "id_region": region_test.id_region
            },
            params={"id_comuna": 99999}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe comuna con ese id"
