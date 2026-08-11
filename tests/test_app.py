from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    activity = "Chess Club"
    email = "duplicate.student@mergington.edu"

    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200

    second_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant():
    activity = "Chess Club"
    email = "remove.me@mergington.edu"

    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
