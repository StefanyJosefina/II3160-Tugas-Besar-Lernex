def test_create_record(client, auth_headers):
    payload = {
        "learner_id": "l-1",
        "completed_course_ids": ["c-1"],
        "ongoing_course_ids": ["c-2"]
    }
    response = client.post("/learning-records/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["completed_course_ids"]) == 1

def test_list_records(client, auth_headers):
    response = client.get("/learning-records/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)