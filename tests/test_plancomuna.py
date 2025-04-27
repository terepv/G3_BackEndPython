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
class TestPlanComunaEndpoint():
    async def test_get_plan_comuna(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        id_plan = 1
        response = client.get(f"/planes/{id_plan}/comunas", headers=headers)
        assert response.status_code == 200
        data = response.json()
    
    async def test_post_delete_planes_comunas(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        id_plan = 1
        id_comuna = 1

       # 2. Crear plan para una comuna (POST)
        post_payload = {
         "id_plan": id_plan,
         "id_comuna": id_comuna
        
        }
        post_response = client.post(f"/planes/{id_plan}/comunas/{id_comuna}", headers=headers, json=post_payload)
        assert post_response.status_code in (201, 409)

        #3. Elimina un plan para la columna
        delete_response = client.delete(f"/planes/{id_plan}/comunas/{id_comuna}", headers=headers)
        assert delete_response.status_code == 200

        

