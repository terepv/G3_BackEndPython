import pytest
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, get_basic_auth_header, password_admin,
    email_fiscalizador, password_fiscalizador, email_organismo_sectorial, password_organismo_sectorial,
    creado_por
)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestOpcionesEndpoints():
    # ####################################################
    # GET /opciones
    # ####################################################
    async def test_admin_get_opciones_success(self, client):
        """Un usuario admin puede obtener todas las opciones."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/opciones/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_fiscalizador_get_opciones_success(self, client):
        """Un usuario fiscalizador puede obtener todas las opciones."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/opciones/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_organismo_sectorial_get_opciones_success(self, client):
        """Un usuario organismo sectorial puede obtener todas las opciones."""
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/opciones/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_opciones_unauthorized(self, client):
        """Un usuario no autenticado no puede acceder al endpoint."""
        response = client.get("/opciones/")
        assert response.status_code == 401
        assert response.json().get("detail") == "Credenciales invalidas"

    # ####################################################
    # POST /opciones
    # ####################################################
    async def test_admin_create_opcion_success(self, client):
        """Un usuario admin puede crear una opción."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.post("/opciones/", headers=headers, json={
            "opcion": "Nueva Opción Test"
        })
        assert response.status_code == 201
        assert response.json()["message"] == "Se creó opcion"
        
        # Limpiar: eliminar la opción creada
        opcion_id = response.json()["opcion"]["id_opcion"]
        client.delete(f"/opciones/{opcion_id}", headers=headers)

    async def test_admin_create_opcion_empty_fails(self, client):
        """No se puede crear una opción vacía."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.post("/opciones/", headers=headers, json={
            "opcion": ""
        })
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "string_too_short"

    async def test_admin_create_opcion_too_long_fails(self, client):
        """No se puede crear una opción demasiado larga."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.post("/opciones/", headers=headers, json={
            "opcion": "x" * 101  # Más de 100 caracteres
        })
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "string_too_long"

    # ####################################################
    # PUT /opciones/{id_opcion}
    # ####################################################
    async def test_admin_update_opcion_success(self, client):
        """Un usuario admin puede actualizar una opción."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Primero crear una opción
        create_response = client.post("/opciones/", headers=headers, json={
            "opcion": "Opción para Actualizar"
        })
        opcion_id = create_response.json()["opcion"]["id_opcion"]
        
        # Actualizar la opción
        response = client.put(f"/opciones/{opcion_id}", headers=headers, json={
            "opcion": "Opción Actualizada"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Se actualizó opción"
        assert response.json()["opcion"]["opcion"] == "Opción Actualizada"
        
        # Limpiar: eliminar la opción
        client.delete(f"/opciones/{opcion_id}", headers=headers)

    async def test_admin_update_nonexistent_opcion_fails(self, client):
        """No se puede actualizar una opción que no existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.put("/opciones/99999", headers=headers, json={
            "opcion": "Opción Inexistente"
        })
        assert response.status_code == 404
        assert response.json()["detail"] == "Opción no encontrada"

    # ####################################################
    # DELETE /opciones/{id_opcion}
    # ####################################################
    async def test_admin_delete_opcion_success(self, client):
        """Un usuario admin puede eliminar una opción."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Primero crear una opción
        create_response = client.post("/opciones/", headers=headers, json={
            "opcion": "Opción para Eliminar"
        })
        opcion_id = create_response.json()["opcion"]["id_opcion"]
        
        # Eliminar la opción
        response = client.delete(f"/opciones/{opcion_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Se eliminó opción"

        # Verificar que la opción no aparece en la lista
        response = client.get("/opciones/", headers=headers)
        opciones = response.json()
        assert not any(o["id_opcion"] == opcion_id for o in opciones)

    async def test_fiscalizador_delete_opcion_fails(self, client):
        """Un usuario fiscalizador no puede eliminar una opción."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.delete("/opciones/1", headers=headers)
        assert response.status_code == 401
        assert "No tiene permisos" in response.json()["detail"]
