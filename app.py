from fastapi import FastAPI, HTTPException

app = FastAPI(title="Activities API")

# Sample activities and their registered participants
activities = {
    "coding": ["ruchitha@example.com", "nikhil@example.com"],
    "music": ["student@example.com"],
}


@app.get("/")
def home():
    return {"message": "Welcome to the Activities API"}


@app.post("/activities/{activity_name}/signup")
def signup(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(
            status_code=404,
            detail=f"Activity '{activity_name}' not found",
        )

    if email in activities[activity_name]:
        raise HTTPException(
            status_code=400,
            detail=f"Email '{email}' is already registered",
        )

    activities[activity_name].append(email)

    return {
        "message": f"Successfully registered {email} for {activity_name}"
    }

@app.post("/activities/{activity_name}/unregister")
def unregister(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    if email not in activities[activity_name]:
        raise HTTPException(status_code=400, detail="Not registered for this activity")

    activities[activity_name].remove(email)

    return {"message": f"Successfully unregistered {email} from {activity_name}"}

# Tests for unregister endpoint
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)


def test_unregister_happy_path():
    # Register a participant first
    response = client.post("/activities/coding/signup", params={"email": "test@example.com"})
    assert response.status_code == 200

    # Now unregister the participant
    response = client.post("/activities/coding/unregister", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully unregistered test@example.com from coding"}


def test_unregister_activity_not_found():
    response = client.post("/activities/unknown/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_not_registered():
    response = client.post("/activities/coding/unregister", params={"email": "unregistered@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Not registered for this activity"}
