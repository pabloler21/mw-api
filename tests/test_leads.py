from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

import app.api.leads as leads_module
from app.main import app

client = TestClient(app)

VALID_LEAD = {
    "name": "Juan Perez",
    "company": "Importadora XYZ",
    "email": "juan@xyz.com",
    "product": "olive oil",
}

PATCH_INSERT = "app.api.leads.insert_lead"
PATCH_NOTIFY = "app.api.leads.send_lead_notification"


@pytest.fixture(autouse=True)
def reset_rate_limit():
    leads_module._rate_limit.clear()
    yield
    leads_module._rate_limit.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_submit_lead_valid():
    with (
        patch(PATCH_INSERT, new_callable=AsyncMock, return_value=True),
        patch(PATCH_NOTIFY, new_callable=AsyncMock, return_value=True),
    ):
        response = client.post("/api/leads", json=VALID_LEAD)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_submit_lead_missing_required_fields():
    response = client.post("/api/leads", json={"name": "Juan Perez"})
    assert response.status_code == 422


def test_submit_lead_invalid_email():
    response = client.post("/api/leads", json={**VALID_LEAD, "email": "not-an-email"})
    assert response.status_code == 422


def test_submit_lead_supabase_failure():
    with (
        patch(PATCH_INSERT, new_callable=AsyncMock, return_value=False),
        patch(PATCH_NOTIFY, new_callable=AsyncMock, return_value=True),
    ):
        response = client.post("/api/leads", json=VALID_LEAD)
    assert response.status_code == 500


def test_submit_lead_rate_limit():
    with (
        patch(PATCH_INSERT, new_callable=AsyncMock, return_value=True),
        patch(PATCH_NOTIFY, new_callable=AsyncMock, return_value=True),
    ):
        for _ in range(5):
            client.post("/api/leads", json=VALID_LEAD)
        response = client.post("/api/leads", json=VALID_LEAD)
    assert response.status_code == 429


def test_submit_lead_optional_fields():
    with (
        patch(PATCH_INSERT, new_callable=AsyncMock, return_value=True),
        patch(PATCH_NOTIFY, new_callable=AsyncMock, return_value=True),
    ):
        response = client.post("/api/leads", json={
            **VALID_LEAD,
            "destination_port": "Dubai",
            "message": "Interested in bulk order.",
        })
    assert response.status_code == 200
    assert response.json()["success"] is True
