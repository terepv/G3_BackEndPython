import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
)


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
class TestTipoMedidasEndpoints():
    async def test_admin_get_planes_comuna_success(self, client):
        headers = get_basic_auth_header(email_admin, password_admin)
        response = client.post("/auth/token", headers=headers)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/planes/", headers=headers)
        assert response.status_code == 200

    async def test_crud_planes_comuna_success(self, client):
        plan_name = f"plan_test"

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
            plan = get_or_create("/planes/", {
                "nombre": plan_name,
                "descripcion": "Descripcion del plan test",
                "fecha_publicacion": "2025-04-20 17:02:00",
            }, "nombre", "id_plan", access_token, "plan")
            assert plan["nombre"] == plan_name
            assert plan["id_plan"] is not None


            comuna = get_or_create("/comunas/", {
                "comuna": "Arica",
            }, "comuna", "id_comuna", access_token)
            assert comuna["comuna"] == "Arica"
            assert comuna["id_comuna"] is not None

            headers = {"Authorization": f"Bearer {access_token}"}
            response = client.post(f"/planes/{plan['id_plan']}/comunas/{comuna['id_comuna']}/", headers=headers)
            assert response.status_code in (200, 201)
            created_resources.append((f"/planes/{plan['id_plan']}/comunas/", comuna['id_comuna']))

            response = client.post(f"/planes/{plan['id_plan']}/comunas/{comuna['id_comuna']}/", headers=headers)
            assert response.status_code == 409
            assert response.json()["detail"] == "La comuna ya está asociada al plan"


        finally:
            headers = {"Authorization": f"Bearer {access_token}"}
            for endpoint, resource_id in reversed(created_resources):
                # print(f"Deleting {endpoint}{resource_id}")
                delete_response = client.delete(f"{endpoint}{resource_id}/", headers=headers)
                assert delete_response.status_code in (200, 204), f"Error deleting {endpoint}{resource_id}"