import pytest
from base64 import b64encode
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, password_admin,
)


def get_basic_auth_header(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

class TestFrecuencias():
    def test_get_frecuencia_without_credentials(self, client):
        response = client.get("/frecuencias")
        assert response.status_code == 401
        assert response.json() == {"detail": "Credenciales invalidas"}

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestFrecuenciasAsync():
    async def test_get_frecuencias(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/frecuencias", headers=headers)
        assert response.status_code == 200
        data = response.json()