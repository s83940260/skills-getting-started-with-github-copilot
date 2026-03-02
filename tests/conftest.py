"""Shared pytest fixtures for the activity signup API tests."""

from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def sample_activities():
    """Provides a fresh copy of activities data for each test."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def test_client(sample_activities):
    """Provides a TestClient with isolated activities data for each test."""
    # Create a fresh FastAPI app for this test
    app = FastAPI()
    
    # Use the sample activities
    activities = sample_activities
    
    # Define endpoints with the isolated activities
    @app.get("/")
    def root():
        return RedirectResponse(url="/static/index.html")

    @app.get("/activities")
    def get_activities():
        return activities

    @app.post("/activities/{activity_name}/signup")
    def signup_for_activity(activity_name: str, email: str):
        """Sign up a student for an activity"""
        # Validate activity exists
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Get the specific activity
        activity = activities[activity_name]

        # Validate student is not already signed up
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student already signed up for this activity")

        # Add student
        activity["participants"].append(email)
        return {"message": f"Signed up {email} for {activity_name}"}

    @app.delete("/activities/{activity_name}/signup")
    def unregister_from_activity(activity_name: str, email: str):
        """Unregister a student from an activity"""
        # Validate activity exists
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Get the specific activity
        activity = activities[activity_name]

        # Validate student is signed up
        if email not in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        # Remove student
        activity["participants"].remove(email)
        return {"message": f"Unregistered {email} from {activity_name}"}

    return TestClient(app)
