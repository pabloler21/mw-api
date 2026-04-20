from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_submit_lead():
    response = client.post("/api/leads", json={
        "name": "Juan Perez",
        "company": "Importadora XYZ",
        "email": "juan@xyz.com",
        "product": "olive oil",
    })
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_submit_lead_missing_required_fields():
    response = client.post("/api/leads", json={
        "name": "Juan Perez",
    })
    assert response.status_code == 422


def test_submit_lead_invalid_email():
    response = client.post("/api/leads", json={
        "name": "Juan Perez",
        "company": "Importadora XYZ",
        "email": "not-an-email",
        "product": "olive oil",
    })
    assert response.status_code == 422


def test_submit_lead_optional_fields():
    response = client.post("/api/leads", json={
        "name": "Ana Garcia",
        "company": "Global Trade SA",
        "email": "ana@globaltrade.com",
        "product": "alfalfa",
        "destination_port": "Dubai",
        "message": "Interested in bulk order.",
    })
    assert response.status_code == 200
    assert response.json()["success"] is True
