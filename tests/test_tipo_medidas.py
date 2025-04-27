import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
    email_fiscalizador, password_fiscalizador, 
    email_organismo_sectorial, password_organismo_sectorial,
    tipo_medida_name, delete_tipo_medida_if_exists, tipo_medida_test
)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
@pytest.mark.usefixtures("delete_tipo_medida_if_exists")
class TestTipoMedidasEndpoints():
    # ####################################################
    # GET /tipo_medidas
    # ####################################################
    async def test_admin_get_tipos_medidas_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/tipo_medidas/", headers=headers)
        assert response.status_code == 200

    async def test_fiscalizador_get_tipos_medidas_success(self, client):
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/tipo_medidas/", headers=headers)
        assert response.status_code == 200

    async def test_organismo_sectorial_get_tipos_medidas_success(self, client):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/tipo_medidas/", headers=headers)
        assert response.status_code == 200

    # ####################################################
    # POST /tipo_medidas
    # ####################################################
    async def test_admin_post_tipos_medidas_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/tipo_medidas/", headers=headers, json={"tipo_medida": tipo_medida_name})
        assert response.status_code == 201

    async def test_fiscalizador_post_tipos_medidas_fail(self, client):
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/tipo_medidas/", headers=headers, json={"tipo_medida": tipo_medida_name})
        assert response.status_code == 401
        assert response.json() == {
            "detail": "No tiene permisos para acceder a este recurso"
        }

    async def test_organismo_sectorial_post_tipos_medidas_fail(self, client):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/tipo_medidas/", headers=headers, json={"tipo_medida": tipo_medida_name})
        assert response.status_code == 401
        assert response.json() == {
            "detail": "No tiene permisos para acceder a este recurso"
        }
    
    # ####################################################
    # GET /tipo_medidas/{id_tipo_medida}
    # ####################################################
    async def test_admin_get_tipo_medida_success(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers)
        assert response.status_code == 200

    async def test_fiscalizador_get_tipo_medida_success(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers)
        assert response.status_code == 200

    async def test_organismo_sectorial_get_tipo_medida_success(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers)
        assert response.status_code == 200

    # ####################################################
    # PUT /tipo_medidas/{id_tipo_medida}
    # ####################################################
    async def test_admin_put_tipo_medida_success(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers, json={"tipo_medida": f"{tipo_medida_name}_updated"})
        assert response.status_code == 200
        response = client.put(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers, json={"tipo_medida": tipo_medida_name})
        assert response.status_code == 200

    async def test_fiscalizador_put_tipo_medida_fail(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers, json={"tipo_medida": f"{tipo_medida_name}_updated"})
        assert response.status_code == 401

    async def test_organismo_sectorial_put_tipo_medida_fail(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers, json={"tipo_medida": f"{tipo_medida_name}_updated"})
        assert response.status_code == 401

    # ####################################################
    # DELETE /tipo_medidas/{id_tipo_medida}
    # ####################################################
    async def test_admin_delete_tipo_medida_success(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.delete(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers)
        assert response.status_code == 200

    async def test_fiscalizador_delete_tipo_medida_fail(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.delete(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers)
        assert response.status_code == 401

    async def test_organismo_sectorial_delete_tipo_medida_fail(self, client, tipo_medida_test):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.delete(f"/tipo_medidas/{tipo_medida_test.id_tipo_medida}", headers=headers)
        assert response.status_code == 401