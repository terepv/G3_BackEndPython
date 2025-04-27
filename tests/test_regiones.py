import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
)


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestRegionesEndpoints():
    async def test_admin_get_regiones_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/regiones/", headers=headers)
        assert response.status_code == 200

    async def test_crud_regiones_success(self, client):
        
        region_name = f"region_test"

        created_resources = []

        def get_or_create(endpoint, payload, name_field, id_field, access_token, post_object: str = None):
            headers = {"Authorization": f"Bearer {access_token}"}
            get_response = client.get(endpoint, headers=headers)
            assert get_response.status_code == 200
            existing = next((item for item in get_response.json() if item.get(name_field) == payload[name_field]), None)
            if existing:
                return existing
            post_response = client.post(endpoint, headers=headers, json=payload)
            assert post_response.status_code in (200, 201)
            resource = post_response.json()[post_object if post_object else name_field]
            created_resources.append((endpoint, resource[id_field]))
            return resource
        
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        
        try: 
            region = get_or_create("/regiones/", {
                "region": region_name,
            }, "region", "id_region", access_token, "región")
            assert region["region"] == region_name
            assert region["id_region"] is not None

            headers = {"Authorization": f"Bearer {access_token}"}
            response = client.put(f"/regiones/{region['id_region']}", headers=headers, json={
                "region": "region_test_editado",
            })
            assert response.status_code == 200
            region_editada = response.json()["región"]
            assert region_editada["region"] == "region_test_editado"

        finally:
            headers = {"Authorization": f"Bearer {access_token}"}
            for endpoint, resource_id in reversed(created_resources):
                # print(f"Deleting {endpoint}{resource_id}")
                delete_response = client.delete(f"{endpoint}{resource_id}/", headers=headers)
                assert delete_response.status_code in (200, 204), f"Error deleting {endpoint}{resource_id}"