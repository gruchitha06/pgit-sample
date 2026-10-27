from fastapi import FastAPI, HTTPException

app = FastAPI(title="Activities API")

# Sample activities and their registered participants
activities = {
    "coding": ["ruchitha@example.com", "nikhil@example.com"],
    "music": ["student@example.com"],
}


@app.get("/")
def home():
    return {"message": "Welcome to the Activities"}


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

    return {"message": f"Successfully unregistered {email} from {activity_name}"}
