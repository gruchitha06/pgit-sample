from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_unregister_success():
    # Register first to ensure the email is in the participant list
    response = client.post("/activities/coding/signup", params={"email": "testuser@example.com"})
    assert response.status_code == 200

    # Now unregister
    response = client.post("/activities/coding/unregister", params={"email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully unregistered testuser@example.com from coding"}


def test_unregister_activity_not_found():
    response = client.post("/activities/nonexistent/unregister", params={"email": "someone@example.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered():
    response = client.post("/activities/music/unregister", params={"email": "unknown@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Not registered for this activity"
