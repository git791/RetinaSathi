import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from app.routes.screening import explanation_service

client = TestClient(app)

valid_payload = {
    "screeningId": "test-id",
    "status": "COMPLETED",
    "quality": {
        "status": "GOOD",
        "score": 0.9,
        "focusScore": 0.9,
        "illuminationScore": 0.9,
        "fovScore": 0.9,
        "fovFraction": 0.9,
        "action": "PROCEED",
        "message": ""
    },
    "aiResult": {
        "predictedLevel": 3,
        "predictedClass": "Severe DR",
        "confidence": 0.69,
        "referable": True,
        "referralStatus": "REFERABLE",
        "recommendation": ""
    },
    "explainability": {
        "type": "GRAD_CAM",
        "image": "base64"
    }
}

ungradable_payload = {
    "screeningId": "test-id",
    "status": "UNGRADABLE",
    "quality": {
        "status": "UNGRADABLE",
        "score": 0.1,
        "focusScore": 0.1,
        "illuminationScore": 0.1,
        "fovScore": 0.1,
        "fovFraction": 0.1,
        "action": "RECAPTURE",
        "message": ""
    },
    "aiResult": None,
    "explainability": None
}

def test_explain_development_mode():
    explanation_service.enabled = False
    
    response = client.post("/api/v1/explain", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Development Mode" in data["explanation"]
    assert data["model"] == "mock-explanation"

def test_explain_no_api_key():
    explanation_service.enabled = True
    explanation_service.client = None
    
    response = client.post("/api/v1/explain", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "AI explanation service unavailable"

def test_explain_ungradable():
    explanation_service.enabled = True
    explanation_service.client = MagicMock()
    
    response = client.post("/api/v1/explain", json=ungradable_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "ungradable" in data["explanation"].lower()
    
def test_explain_api_failure():
    explanation_service.enabled = True
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("API Error")
    explanation_service.client = mock_client
    
    response = client.post("/api/v1/explain", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "AI explanation service unavailable"
    
def test_explain_success():
    explanation_service.enabled = True
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a detailed clinical explanation."
    mock_client.models.generate_content.return_value = mock_response
    explanation_service.client = mock_client
    
    response = client.post("/api/v1/explain", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["explanation"] == "This is a detailed clinical explanation."
