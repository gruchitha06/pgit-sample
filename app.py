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


def unregister(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(
            status_code=404,
            detail="Activity not found",
        )

    if email not in activities[activity_name]:
        raise HTTPException(
            status_code=400,
            detail="Not registered for this activity",
        )

    activities[activity_name].remove(email)

    return {
        "message": f"Successfully unregistered {email} from {activity_name}"
    }


# Simple test functions
if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)

    def test_unregister_happy():
        # Precondition: "ruchitha@example.com" is registered for coding
        response = client.post("/activities/coding/unregister", params={"email": "ruchitha@example.com"})
        assert response.status_code == 200
        assert response.json() == {"message": "Successfully unregistered ruchitha@example.com from coding"}
        # Verify removal
        response_check = client.post("/activities/coding/unregister", params={"email": "ruchitha@example.com"})
        assert response_check.status_code == 400
        assert response_check.json() == {"detail": "Not registered for this activity"}

    def test_unregister_validation():
        response = client.post("/activities/music/unregister", params={"email": "notregistered@example.com"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Not registered for this activity"}

    # Run tests
    test_unregister_happy()
    test_unregister_validation()

    print("All tests passed.")
