"""
PyTest fixtures for FastAPI test client and application setup.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Create a test client using FastAPI's TestClient.
    This fixture will be used by test functions to make requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def test_activity():
    """
    Return a test activity data structure for use in tests.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["test1@mergington.edu", "test2@mergington.edu"]
        }
    }