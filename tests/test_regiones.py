import pytest
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, get_basic_auth_header, password_admin,
    email_fiscalizador, password_fiscalizador, email_organismo_sectorial, password_organismo_sectorial,
    creado_por, region_test_name, delete_region_if_exists, region_test
)
from datetime import datetime

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
@pytest.mark.usefixtures("delete_region_if_exists")
class TestRegionesEndpoints():
    # ####################################################
    # GET /regiones
    # ####################################################
    async def test_admin_get_regiones_success(self, client):
        """Un usuario admin puede obtener todas las regiones."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/regiones/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_fiscalizador_get_regiones_success(self, client):
        """Un usuario fiscalizador puede obtener todas las regiones."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/regiones/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_organismo_sectorial_get_regiones_success(self, client):
        """Un usuario organismo sectorial puede obtener todas las regiones."""
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/regiones/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_regiones_unauthorized(self, client):
        """Un usuario no autenticado no puede acceder al endpoint."""
        response = client.get("/regiones/")
        assert response.status_code == 401
        assert response.json().get("detail") == "Credenciales invalidas"

    # ####################################################
    # GET /regiones/{id_region}
    # ####################################################
    async def test_admin_get_region_success(self, client, region_test):
        """Un usuario admin puede obtener una región específica."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/regiones/{region_test.id_region}", headers=headers)
        assert response.status_code == 200
        assert response.json()["region"] == region_test_name

    async def test_fiscalizador_get_region_success(self, client, region_test):
        """Un usuario fiscalizador puede obtener una región específica."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/regiones/{region_test.id_region}", headers=headers)
        assert response.status_code == 200
        assert response.json()["region"] == region_test_name

    async def test_get_region_not_found(self, client):
        """Obtener una región que no existe devuelve 404."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/regiones/99999", headers=headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe región con ese id"

    # ####################################################
    # POST /regiones
    # ####################################################
    async def test_admin_create_region_success(self, client):
        """Un usuario admin puede crear una región."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        new_region_name = f"Nueva Región {datetime.now().strftime('%Y%m%d%H%M%S')}"
        response = client.post("/regiones/", headers=headers, json={"region": new_region_name})
        assert response.status_code == 201
        assert response.json()["región"]["region"] == new_region_name

    async def test_admin_create_existing_region_fails(self, client, region_test):
        """No se puede crear una región que ya existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/regiones/", headers=headers, json={"region": region_test_name})
        assert response.status_code == 409
        assert response.json()["detail"] == "Región ya existe"

    async def test_fiscalizador_create_region_unauthorized(self, client):
        """Un usuario fiscalizador no puede crear una región."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/regiones/", headers=headers, json={"region": "Nueva Región"})
        assert response.status_code == 401
        assert response.json() == {"detail": "No tiene permisos para acceder a este recurso"}

    # ####################################################
    # PUT /regiones/{id_region}
    # ####################################################
    async def test_admin_update_region_success(self, client, region_test):
        """Un usuario admin puede actualizar una región."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        updated_name = f"{region_test_name}_updated"
        response = client.put(
            f"/regiones/{region_test.id_region}", 
            headers=headers, 
            json={"region": updated_name}
        )
        assert response.status_code == 200
        assert response.json()["región"]["region"] == updated_name

        # Restaurar nombre original
        response = client.put(
            f"/regiones/{region_test.id_region}", 
            headers=headers, 
            json={"region": region_test_name}
        )
        assert response.status_code == 200

    async def test_admin_update_nonexistent_region_fails(self, client):
        """No se puede actualizar una región que no existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/regiones/99999", headers=headers, json={"region": "Nueva Región"})
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe región con ese id"

    async def test_fiscalizador_update_region_unauthorized(self, client, region_test):
        """Un usuario fiscalizador no puede actualizar una región."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put(
            f"/regiones/{region_test.id_region}", 
            headers=headers, 
            json={"region": "Región Actualizada"}
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "No tiene permisos para acceder a este recurso"}

    # ####################################################
    # DELETE /regiones/{id_region}
    # ####################################################
    async def test_admin_delete_region_success(self, client, region_test):
        """Un usuario admin puede eliminar una región."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.delete(f"/regiones/{region_test.id_region}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Se eliminó región"}

    async def test_fiscalizador_delete_region_unauthorized(self, client, region_test):
        """Un usuario fiscalizador no puede eliminar una región."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.delete(f"/regiones/{region_test.id_region}", headers=headers)
        assert response.status_code == 401
        assert response.json() == {"detail": "No tiene permisos para acceder a este recurso"}