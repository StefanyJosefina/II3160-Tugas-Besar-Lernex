def test_create_progress(client, auth_headers):
    payload = {
        "learner_id": "l-1",
        "course_id": "course-001",
        "completion_rate": 0.5,
        "status": "IN_PROGRESS"
    }
    response = client.post("/progress/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["completion_rate"] == 0.5

def test_get_progress_by_id(client, auth_headers):
    payload = {
        "learner_id": "l-1",
        "course_id": "course-001",
        "status": "IN_PROGRESS"
    }
    create_res = client.post("/progress/", json=payload, headers=auth_headers)
    progress_id = create_res.json()["progress_id"]
    
    response = client.get(f"/progress/{progress_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["progress_id"] == progress_id