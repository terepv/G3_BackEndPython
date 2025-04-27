import pytest
from base64 import b64encode
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, password_admin,
)

def get_basic_auth_header(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestRegionesEndpoint():
    async def test_get_regiones(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/regiones", headers=headers)
        assert response.status_code == 200
        data = response.json()

    async def test_post_put_delete_regiones(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

       # 2. Crear región (POST)
        post_payload = {
            "region": "Región Ficticia",
        }

        post_response = client.post("/regiones", headers=headers, json=post_payload)
        assert post_response.status_code == 201
        region_data = post_response.json()
        region_id = region_data["región"]["id_region"]
        assert region_id is not None

        # 3. Actualizar región (PUT)
        put_payload = {
            "region":"Region Ficticia actualizada"
        }
        
        put_response = client.put(f"/regiones/{region_id}", headers=headers, json=put_payload)
        assert put_response.status_code == 200

        # 4. Eliminar región (DELETE)
        delete_response = client.delete(f"/regiones/{region_id}", headers=headers)
        assert delete_response.status_code == 204 or delete_response.status_code == 200

        # 5. Verificar que fue eliminada (GET debe fallar o dar 404)
        get_response = client.get(f"/regiones/{region_id}", headers=headers)
        assert get_response.status_code == 404

