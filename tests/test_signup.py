"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for activity signup endpoint."""

    def test_successful_signup_returns_200(self, test_client):
        """Test that successful signup returns 200 status code."""
        # Arrange
        activity = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        response = test_client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200

    def test_successful_signup_returns_correct_message(self, test_client):
        """Test that signup returns correct success message."""
        # Arrange
        activity = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        response = test_client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_adds_email_to_participants(self, test_client):
        """Test that signup actually adds the email to participants list."""
        # Arrange
        activity = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        test_client.post(f"/activities/{activity}/signup?email={email}")
        response = test_client.get("/activities")

        # Assert
        participants = response.json()[activity]["participants"]
        assert email in participants

    def test_signup_for_nonexistent_activity_returns_404(self, test_client):
        """Test that signup for non-existent activity returns 404."""
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = test_client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_duplicate_signup_returns_400(self, test_client):
        """Test that signing up twice returns 400 error."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = test_client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_duplicate_signup_does_not_add_duplicate(self, test_client):
        """Test that duplicate signup doesn't add email twice to participants."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        test_client.post(f"/activities/{activity}/signup?email={email}")
        response = test_client.get("/activities")

        # Assert
        participants = response.json()[activity]["participants"]
        count = participants.count(email)
        assert count == 1  # Should still be only 1, not 2

    def test_signup_with_special_characters_in_email(self, test_client):
        """Test that signup works with special characters in email."""
        # Arrange
        activity = "Gym Class"
        email = "student+tag@mergington.edu"

        # Act
        response = test_client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
