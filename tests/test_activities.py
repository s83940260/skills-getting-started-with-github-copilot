"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities list."""

    def test_get_activities_returns_all_activities(self, test_client):
        """Test that activities endpoint returns all activities."""
        # Arrange
        expected_activity_count = 3

        # Act
        response = test_client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert len(response.json()) == expected_activity_count

    def test_activities_have_required_fields(self, test_client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = test_client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"

    def test_participants_list_is_correct(self, test_client):
        """Test that participants list contains expected emails."""
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        expected_gym_participants = []

        # Act
        response = test_client.get("/activities")
        activities = response.json()

        # Assert
        assert activities["Chess Club"]["participants"] == expected_chess_participants
        assert activities["Gym Class"]["participants"] == expected_gym_participants

    def test_max_participants_is_integer(self, test_client):
        """Test that max_participants is an integer."""
        # Arrange
        # Act
        response = test_client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0
