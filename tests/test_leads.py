from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_submit_lead():
    lead_data = {
        "nombre": "Juan Perez",
        "empresa": "Importadora XYZ",
        "email": "juan@xyz.com",
        "producto": "aceite de oliva",
    }
    response = client.post("/api/leads", json=lead_data)
    assert response.status_code == 200
    assert response.json()["success"] is True
