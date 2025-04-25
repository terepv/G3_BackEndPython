import pytest
from base64 import b64encode
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, password_admin,
    email_organismo_sectorial, password_organismo_sectorial
)

def get_basic_auth_header(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestAuthEndpoints():
    async def test_get_token_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"


    async def test_get_token_invalid_credentials(self, client):
        headers = get_basic_auth_header(email_admin, "invalid_password")
        response = client.post("/auth/token", headers=headers)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Credenciales invalidas"
        }

    async def test_refresh_token_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        refresh_token = data["refresh_token"]
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = client.post("/auth/refresh", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "refresh_token" not in data 

    async def test_refresh_token_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/auth/refresh", headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Token invalido'}

    async def test_refresh_token_invalid_token_type(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/auth/refresh", headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'El token provisto no es un token de refresco'}

    async def test_get_me_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == email_admin

    async def test_get_me_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Token invalido'}

    async def test_token_organismo_sectorial_success(self, client):
        headers = get_basic_auth_header(email_organismo_sectorial, password_organismo_sectorial)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "organismo_sectorial" in data["user"]