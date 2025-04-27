import pytest
from base64 import b64encode
from utils.conftest import (
    create_and_delete_test_users, client, email_admin, password_admin,
)
from uuid import uuid4

def get_basic_auth_header(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestTipoDatoEndpoint():
    async def test_get_tipo_dato(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/tipos_datos", headers=headers)
        assert response.status_code == 200
        data = response.json()

    async def test_post_put_delete_tipo_dato(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        data = response.json()
        access_token = data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

       # 2. Crear tipo dato (POST)
        post_payload = {
        "tipo_dato": f"Tipo Dato Ficticio {uuid4().hex[:6]}"
        }

        post_response = client.post("/tipos_datos", headers=headers, json=post_payload)
        assert post_response.status_code == 201
        tipo_dato_data = post_response.json()
        tipo_dato_id = tipo_dato_data["Tipo de dato"]["id_tipo_dato"]
        
        assert tipo_dato_id is not None

        # 3. Actualizar región (PUT)
        put_payload = {
        "tipo_dato": f"Tipo Dato Ficticio Actualizada {uuid4().hex[:6]}"
        }
        
        put_response = client.put(f"/tipos_datos/{tipo_dato_id}", headers=headers, json=put_payload)
        assert put_response.status_code == 201

        # 4. Eliminar región (DELETE)
        delete_response = client.delete(f"/tipos_datos/{tipo_dato_id}", headers=headers)
        assert delete_response.status_code == 200
