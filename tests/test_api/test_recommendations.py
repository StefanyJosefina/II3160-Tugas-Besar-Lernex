def test_create_recommendation(client, auth_headers):
    payload = {
        "learner_id": "l-1",
        "course_ids": ["course-001", "course-002"]
    }
    response = client.post("/recommendations/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["course_ids"]) == 2

def test_get_recommendation_by_id(client, auth_headers):
    payload = {
        "learner_id": "l-1",
        "course_ids": ["c-1"]
    }
    create_res = client.post("/recommendations/", json=payload, headers=auth_headers)
    rec_id = create_res.json()["recommendation_id"]
    
    response = client.get(f"/recommendations/{rec_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["recommendation_id"] == rec_id