import pytest
from datetime import datetime
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, get_basic_auth_header, password_admin,
    email_fiscalizador, password_fiscalizador, email_organismo_sectorial, password_organismo_sectorial,
    creado_por
)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestUsuariosEndpoints():
    # ####################################################
    # GET /usuarios
    # ####################################################
    async def test_admin_get_usuarios_success(self, client):
        """Un usuario admin puede obtener todos los usuarios."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/usuarios/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_fiscalizador_get_usuarios_fails(self, client):
        """Un usuario fiscalizador no puede obtener todos los usuarios."""
        headers = get_basic_auth_header(email_fiscalizador, password_fiscalizador)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/usuarios/", headers=headers)
        assert response.status_code == 401
        assert "No tiene permisos" in response.json()["detail"]

    async def test_get_usuarios_unauthorized(self, client):
        """Un usuario no autenticado no puede acceder al endpoint."""
        response = client.get("/usuarios/")
        assert response.status_code == 401
        assert response.json().get("detail") == "Credenciales invalidas"

    # ####################################################
    # GET /usuarios/{id_usuario}
    # ####################################################
    async def test_admin_get_usuario_success(self, client):
        """Un usuario admin puede obtener un usuario específico."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Obtener el usuario fiscalizador que ya existe
        response = client.get("/usuarios/", headers=headers)
        usuarios = response.json()
        usuario_fiscalizador = next(u for u in usuarios if u["email"] == email_fiscalizador)
        
        response = client.get(f"/usuarios/{usuario_fiscalizador['id_usuario']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == email_fiscalizador

    async def test_get_usuario_not_found(self, client):
        """Obtener un usuario que no existe devuelve 404."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/usuarios/99999", headers=headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe usuario con ese id"

    # ####################################################
    # POST /usuarios
    # ####################################################
    async def test_admin_create_usuario_success(self, client):
        """Un usuario admin puede crear un usuario."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_user_data = {
            "email": f"test_user_{timestamp}@test.com",
            "nombre": "Test",
            "apellido": "User",
            "password": "testpass123",
            "id_rol": 2,  # Fiscalizador
            "activo": True,
            "id_organismo_sectorial": None
        }
        
        response = client.post("/usuarios/", headers=headers, json=new_user_data)
        assert response.status_code == 201
        assert response.json()["usuario"]["email"] == new_user_data["email"]
        
        # Limpiar: eliminar el usuario creado
        user_id = response.json()["usuario"]["id_usuario"]
        client.delete(f"/usuarios/{user_id}", headers=headers)

    async def test_admin_create_duplicate_usuario_fails(self, client):
        """No se puede crear un usuario con un email que ya existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        user_data = {
            "email": email_fiscalizador,  # Email que ya existe
            "nombre": "Duplicate",
            "apellido": "User",
            "password": "testpass123",
            "id_rol": 2,
            "activo": True,
            "id_organismo_sectorial": None
        }
        
        response = client.post("/usuarios/", headers=headers, json=user_data)
        assert response.status_code == 409
        assert response.json()["detail"] == "Usuario ya existe"

    # ####################################################
    # PUT /usuarios/{id_usuario}
    # ####################################################
    async def test_admin_update_usuario_success(self, client):
        """Un usuario admin puede actualizar un usuario."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Crear usuario de prueba
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_user_data = {
            "email": f"update_user_{timestamp}@test.com",
            "nombre": "Update",
            "apellido": "User",
            "password": "updatepass123",
            "id_rol": 2,
            "activo": True,
            "id_organismo_sectorial": None
        }
        
        create_response = client.post("/usuarios/", headers=headers, json=new_user_data)
        created_user = create_response.json()["usuario"]
        
        # Actualizar usuario
        update_data = dict(new_user_data)
        update_data["nombre"] = "Updated"
        update_data["apellido"] = "UserUpdated"
        
        response = client.put(
            f"/usuarios/{created_user['id_usuario']}", 
            headers=headers, 
            json=update_data
        )
        assert response.status_code == 200
        assert response.json()["usuario"]["nombre"] == "Updated"
        assert response.json()["usuario"]["apellido"] == "UserUpdated"
        
        # Limpiar: eliminar el usuario creado
        client.delete(f"/usuarios/{created_user['id_usuario']}", headers=headers)

    async def test_admin_update_nonexistent_usuario_fails(self, client):
        """No se puede actualizar un usuario que no existe."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        update_data = {
            "email": "nonexistent@test.com",
            "nombre": "NonExistent",
            "apellido": "User",
            "password": "testpass123",
            "id_rol": 2,
            "activo": True,
            "id_organismo_sectorial": None
        }
        
        response = client.put("/usuarios/99999", headers=headers, json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "No existe usuario con ese id"

    # ####################################################
    # DELETE /usuarios/{id_usuario}
    # ####################################################
    async def test_admin_delete_usuario_success(self, client):
        """Un usuario admin puede eliminar un usuario."""
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Crear usuario de prueba
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        test_email = f"delete_user_{timestamp}@test.com"
        new_user_data = {
            "email": test_email,
            "nombre": "Delete",
            "apellido": "User",
            "password": "deletepass123",
            "id_rol": 2,
            "activo": True,
            "id_organismo_sectorial": None
        }

        create_response = client.post("/usuarios/", headers=headers, json=new_user_data)
        created_user = create_response.json()["usuario"]

        # Verificar que el usuario existe en la lista de usuarios
        response = client.get("/usuarios/", headers=headers)
        usuarios_antes = response.json()
        assert any(u["email"] == test_email for u in usuarios_antes)

        # Eliminar usuario
        response = client.delete(f"/usuarios/{created_user['id_usuario']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Se eliminó usuario"

        # Verificar que el usuario ya no aparece en la lista de usuarios activos
        response = client.get("/usuarios/", headers=headers)
        usuarios_despues = response.json()
        assert not any(u["email"] == test_email for u in usuarios_despues)