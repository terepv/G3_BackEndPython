from utils.conftest import client

class TestMain():
    def test_root_response_api_is_running(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "API is running"}

    def test_rate_limit_exceeded(self, client):
        for _ in range(5):
            response = client.get("/")
            assert response.status_code == 200
        response = client.get("/")
        assert response.status_code == 429