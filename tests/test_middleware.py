from fastapi.testclient import TestClient

from rest.app.main import app


def test_health_response_includes_process_time_header() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) >= 0.0
