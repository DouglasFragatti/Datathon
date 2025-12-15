from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running. Go to /docs for Swagger UI."}

def test_predict_endpoint():
    payload = {
        "IAA": 8.5,
        "IEG": 7.0,
        "IPS": 7.5,
        "IDA": 6.0,
        "Matem": 5.5,
        "Portug": 6.5,
        "Inglês": 7.0,
        "IPV": 7.0,
        "IAN": 6.0,
        "Fase_ideal": "Fase 2",
        "Destaque_IEG": "Não",
        "Destaque_IDA": "Não",
        "Destaque_IPV": "Não"
    }
    response = client.post("/predict", json=payload)
    if response.status_code != 200:
        print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
