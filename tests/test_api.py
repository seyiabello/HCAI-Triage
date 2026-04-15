from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "HCAI-Triage API"


def test_predict_high_risk_case() -> None:
    payload = {
        "patient_id": "P001",
        "age": 68,
        "heart_rate": 112,
        "hrv": 18,
        "sleep_hours": 4,
        "steps": 1500,
        "spo2": 93,
        "symptoms": "shortness of breath and chest pain",
        "medical_history": ["hypertension", "heart disease"],
        "patient_preferences": {
            "avoid_hospital": False,
            "cost_sensitive": True,
            "prefers_remote": True
        },
        "clinician_override_requested": False
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["patient_id"] == "P001"
    assert data["risk_level"] in {"medium", "high"}
    assert "recommendation" in data
    assert isinstance(data["top_factors"], list)


def test_predict_low_risk_case() -> None:
    payload = {
        "patient_id": "P002",
        "age": 27,
        "heart_rate": 72,
        "hrv": 55,
        "sleep_hours": 7.5,
        "steps": 7500,
        "spo2": 99,
        "symptoms": "mild cough",
        "medical_history": [],
        "patient_preferences": {
            "avoid_hospital": True,
            "cost_sensitive": False,
            "prefers_remote": True
        },
        "clinician_override_requested": False
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["patient_id"] == "P002"
    assert data["risk_score"] <= 1.0
    assert data["risk_level"] in {"low", "medium", "high"}