def test_list_courses(client, auth_headers):
    response = client.get("/courses/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3 

def test_get_course_detail(client, auth_headers):
    course_id = "course-001"
    response = client.get(f"/courses/{course_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == course_id
    assert "modules" in data

def test_get_course_not_found(client, auth_headers):
    response = client.get("/courses/non-existent-id", headers=auth_headers)
    assert response.status_code == 404

def test_enroll_course(client, auth_headers):
    course_id = "course-001"
    response = client.post(f"/courses/{course_id}/enroll", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully enrolled in course"
    assert data["course_id"] == course_id

def test_enroll_already_exists(client, auth_headers):
    course_id = "course-001"
    client.post(f"/courses/{course_id}/enroll", headers=auth_headers)
    response = client.post(f"/courses/{course_id}/enroll", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Already enrolled in this course"

def test_get_my_courses(client, auth_headers):
    client.post("/courses/course-001/enroll", headers=auth_headers)
    
    response = client.get("/courses/my-courses", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["course_id"] == "course-001"