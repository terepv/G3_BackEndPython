import pytest
from utils.conftest import (
    create_and_delete_test_users, client, get_basic_auth_header,
    email_admin, password_admin,
)

@pytest.mark.asyncio
@pytest.mark.usefixtures("create_and_delete_test_users")
async def test_admin_post_opciones_medidas_success(client):
    opcion_name = f"opcion_test"
    tipo_medida_name = f"tipo_medida_test"
    frecuencia_name = f"frecuencia_test"
    organismo_name = f"organismo_sectorial_test"
    plan_name = f"plan_test"
    medida_name = f"medida_test"

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
        opcion = get_or_create("/opciones/", {"opcion": opcion_name}, "opcion", "id_opcion", access_token)
        tipo_dato = get_or_create("/tipos_datos/", {"tipo_dato": "Selección"}, "tipo_dato", "id_tipo_dato", access_token, "Tipo de dato")
        tipo_medida = get_or_create("/tipo_medidas/", {"tipo_medida": tipo_medida_name}, "tipo_medida", "id_tipo_medida", access_token, "Tipo de medida")
        frecuencia = get_or_create("/frecuencias/", {"frecuencia": frecuencia_name}, "frecuencia", "id_frecuencia", access_token)
        organismo = get_or_create("/organismos_sectoriales/", {"organismo_sectorial": organismo_name}, "organismo_sectorial", "id_organismo_sectorial", access_token)
        plan = get_or_create("/planes/", {
            "nombre": plan_name,
            "descripcion": "Descripcion del plan test",
            "fecha_publicacion": "2025-04-20 17:02:00",
        }, "nombre", "id_plan", access_token, "plan")

        medida_payload = {
            "nombre_corto": medida_name,
            "indicador": "Indicador Test",
            "formula_calculo": "Formula Test",
            "id_frecuencia": frecuencia["id_frecuencia"],
            "id_organismo_sectorial": organismo["id_organismo_sectorial"],
            "id_tipo_medida": tipo_medida["id_tipo_medida"],
            "desc_medio_de_verificacion": "Medio de verificacion Test",
            "id_tipo_dato": tipo_dato["id_tipo_dato"],
            "reporte_unico": False
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post(f"/planes/{plan['id_plan']}/medidas/", headers=headers, json=medida_payload)
        assert response.status_code in (200, 201)
        medida_created = response.json()["medida"]
        created_resources.append((f"/planes/{plan['id_plan']}/medidas/", medida_created["id_medida"]))


        response = client.post("/opciones_medidas/", headers=headers, json={
            "id_opcion": opcion["id_opcion"],
            "id_medida": medida_created["id_medida"],
        })
        assert response.status_code in (200, 201)
        opcion_medida_created = response.json()["opcion_medida"]
        created_resources.append(("/opciones_medidas/", opcion_medida_created["id_opcion_medida"]))

    finally: 
        headers = {"Authorization": f"Bearer {access_token}"}
        for endpoint, resource_id in reversed(created_resources):
            # print(f"Deleting {endpoint}{resource_id}")
            delete_response = client.delete(f"{endpoint}{resource_id}/", headers=headers)
            assert delete_response.status_code in (200, 204), f"Error deleting {endpoint}{resource_id}"



