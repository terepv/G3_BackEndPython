import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
)


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestRolesEndpoints():
    async def test_admin_get_roles_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/roles/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert "Administrador" in [item["rol"] for item in data]
        assert "Fiscalizador" in [item["rol"] for item in data]
        assert "Organismo Sectorial" in [item["rol"] for item in data]

