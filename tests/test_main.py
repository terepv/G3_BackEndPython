from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_response_api_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}