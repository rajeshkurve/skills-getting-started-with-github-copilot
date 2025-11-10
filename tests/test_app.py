"""
Test suite for the FastAPI application endpoints.
Tests cover getting activities, signing up for activities, and removing participants.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_root_redirect(client):
    """Test that the root path redirects to static/index.html"""
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    if response.status_code == 307:  # Redirect
        assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    # Check structure of an activity
    activity = list(activities.values())[0]
    assert all(key in activity for key in ["description", "schedule", "max_participants", "participants"])


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]

    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate(client):
    """Test that signing up a duplicate participant fails"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Using existing participant from the activities data
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    activity_name = "Non-Existent Club"
    email = "new.student@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_participant(client):
    """Test unregistering a participant from an activity"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Using existing participant from the activities data
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]

    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant(client):
    """Test unregistering a non-existent participant"""
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_from_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    activity_name = "Non-Existent Club"
    email = "test1@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()