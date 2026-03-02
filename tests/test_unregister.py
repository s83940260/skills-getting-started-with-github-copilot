"""Tests for the DELETE /activities/{activity_name}/signup endpoint."""

import pytest


class TestUnregisterFromActivity:
    """Test suite for activity unregister endpoint."""

    def test_successful_unregister_returns_200(self, test_client):
        """Test that successful unregister returns 200 status code."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = test_client.delete(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200

    def test_successful_unregister_returns_correct_message(self, test_client):
        """Test that unregister returns correct success message."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = test_client.delete(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_removes_email_from_participants(self, test_client):
        """Test that unregister actually removes the email from participants."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        test_client.delete(f"/activities/{activity}/signup?email={email}")
        response = test_client.get("/activities")

        # Assert
        participants = response.json()[activity]["participants"]
        assert email not in participants

    def test_unregister_from_nonexistent_activity_returns_404(self, test_client):
        """Test that unregister from non-existent activity returns 404."""
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = test_client.delete(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_non_signed_up_student_returns_400(self, test_client):
        """Test that unregistering a non-signed-up student returns 400."""
        # Arrange
        activity = "Gym Class"  # No participants
        email = "notregistered@mergington.edu"

        # Act
        response = test_client.delete(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_student_can_resign_and_re_register(self, test_client):
        """Test that a student can unregister and then re-register."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        # Unregister
        test_client.delete(f"/activities/{activity}/signup?email={email}")
        # Re-register
        response = test_client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        activities_response = test_client.get("/activities")
        participants = activities_response.json()[activity]["participants"]
        assert email in participants
