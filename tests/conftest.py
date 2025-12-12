import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import (
    _learners, 
    _enrollments, 
    _feedback_store, 
    _progress_store, 
    _records, 
    _recommendations
)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
def reset_db():
    _learners.clear()
    _enrollments.clear()
    _feedback_store.clear()
    _progress_store.clear()
    _records.clear()
    _recommendations.clear()
    
    yield

@pytest.fixture
def test_learner_payload():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }

@pytest.fixture
def auth_headers(client, test_learner_payload):
    client.post("/auth/register", json=test_learner_payload)
    
    login_payload = {
        "email": test_learner_payload["email"],
        "password": test_learner_payload["password"]
    }
    response = client.post("/auth/login", json=login_payload)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}