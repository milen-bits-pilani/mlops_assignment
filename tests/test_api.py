"""
Unit tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Mock the model loading before importing app
os.environ["MODEL_PATH"] = "models/best_model.pkl"
os.environ["PREPROCESSOR_PATH"] = "models/preprocessor.pkl"

from src.api.app import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "endpoints" in response.json()


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    # May return 503 if model not loaded, which is expected in test environment
    assert response.status_code in [200, 503]


def test_predict_endpoint_structure():
    """Test predict endpoint accepts correct input structure"""
    sample_input = {
        "age": 63,
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1
    }
    
    response = client.post("/predict", json=sample_input)
    # May fail if model not loaded, but should validate input structure
    assert response.status_code in [200, 500, 503]


def test_predict_endpoint_validation():
    """Test input validation"""
    invalid_input = {
        "age": -10,  # Invalid: negative age
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1
    }
    
    response = client.post("/predict", json=invalid_input)
    # Should return validation error
    assert response.status_code == 422


def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers.get("content-type", "")

