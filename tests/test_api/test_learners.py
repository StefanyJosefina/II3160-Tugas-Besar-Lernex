def test_create_learner_via_router(client):
    payload = {
        "name": "Router User",
        "email": "router@example.com",
        "password": "secretpass"
    }
    response = client.post("/learners/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]

def test_list_learners(client):
    response = client.get("/learners/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_learner_by_id(client):
    payload = {
        "name": "Find Me",
        "email": "findme@example.com",
        "password": "pass"
    }
    create_res = client.post("/learners/", json=payload)
    learner_id = create_res.json()["learner_id"]
    
    response = client.get(f"/learners/{learner_id}")
    assert response.status_code == 200
    assert response.json()["learner_id"] == learner_id

def test_get_learner_not_found(client):
    response = client.get("/learners/invalid-id")
    assert response.status_code == 404