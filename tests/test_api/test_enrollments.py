def test_create_enrollment_direct(client, auth_headers):
    
    payload = {
        "learner_id": "dummy", 
        "course_id": "course-002",
        "status": "ACTIVE"
    }
    response = client.post("/enrollments/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["course_id"] == "course-002"

def test_list_enrollments(client, auth_headers):
    response = client.get("/enrollments/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_enrollment_by_id(client, auth_headers):
    payload = {"learner_id": "l-1", "course_id": "c-1", "status": "ACTIVE"}
    create_res = client.post("/enrollments/", json=payload, headers=auth_headers)
    enrollment_id = create_res.json()["enrollment_id"]
    
    response = client.get(f"/enrollments/{enrollment_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["enrollment_id"] == enrollment_id