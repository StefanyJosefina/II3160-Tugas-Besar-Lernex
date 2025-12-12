def test_register_learner(client):
    response = client.post("/auth/register", json={
        "name": "New User",
        "email": "newuser@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "learner_id" in data

def test_register_duplicate_email(client, test_learner_payload):
    client.post("/auth/register", json=test_learner_payload)
    response = client.post("/auth/register", json=test_learner_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client, test_learner_payload):
    client.post("/auth/register", json=test_learner_payload)
    
    response = client.post("/auth/login", json={
        "email": test_learner_payload["email"],
        "password": test_learner_payload["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_learner_payload):
    client.post("/auth/register", json=test_learner_payload)
    
    response = client.post("/auth/login", json={
        "email": test_learner_payload["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert "email" in response.json()