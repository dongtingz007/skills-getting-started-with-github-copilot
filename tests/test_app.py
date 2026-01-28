import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Tennis Club" in data
    assert "Basketball Team" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_from_activity():
    email = "testuser2@mergington.edu"
    activity = "Art Studio"
    # Sign up first and check response
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": email})
    if signup_response.status_code == 400:
        # Already signed up, so unregister first
        client.post(f"/activities/{activity}/unregister", params={"email": email})
        signup_response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_response.status_code == 200
    # Now unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again (should fail)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
