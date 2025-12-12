def test_create_feedback(client, auth_headers):
    payload = {
        "learner_id": "l-1",
        "course_id": "course-001",
        "comment": "Great course!",
        "rating": {
            "value": 5,
            "comment_category": "content"
        }
    }
    response = client.post("/feedback/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["comment"] == "Great course!"

def test_list_feedback(client, auth_headers):
    response = client.get("/feedback/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)