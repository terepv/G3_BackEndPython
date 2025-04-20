from base64 import b64encode
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from app.main import app
from app.shared.utils import create_access_token, create_refresh_token, get_local_now_datetime

client = TestClient(app)

from os import environ as env

try:
    load_dotenv()
except ImportError:
    pass

def get_basic_auth_header(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

class TestAuthEndpoint:
    def test_get_token_success(self):
        headers = get_basic_auth_header(env["USER_ADMIN"], env["USER_ADMIN_PASSWORD"])
        response = client.post("/auth/token", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_get_token_invalid_credentials(self):
        headers = get_basic_auth_header(env["USER_ADMIN"], "invalid_password")
        response = client.post("/auth/token", headers=headers)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Credenciales invalidas"
        }

    def test_refresh_token_success(self):
        headers = get_basic_auth_header(env["USER_ADMIN"], env["USER_ADMIN_PASSWORD"])
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

    def test_refresh_token_invalid_token(self):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/auth/refresh", headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Token invalido'}

    def test_refresh_token_invalid_token_type(self):
        headers = get_basic_auth_header(env["USER_ADMIN"], env["USER_ADMIN_PASSWORD"])
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/auth/refresh", headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'El token provisto no es un token de refresco'}

    def test_get_me_success(self):
        headers = get_basic_auth_header(env["USER_ADMIN"], env["USER_ADMIN_PASSWORD"])
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == env["USER_ADMIN"]

    def test_get_me_invalid_token(self):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Token invalido'}