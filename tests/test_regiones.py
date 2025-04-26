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
class TestRegionesEndpoints():
    async def test_get_regiones_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        regiones = client.get("/regiones", headers=headers)
        assert regiones.status_code == 200