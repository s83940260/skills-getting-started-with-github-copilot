"""Tests for the GET / (root redirect) endpoint."""

import pytest


class TestRootRedirect:
    """Test suite for root endpoint redirect."""

    def test_root_endpoint_redirects(self, test_client):
        """Test that root endpoint returns a redirect."""
        # Arrange
        # Act
        response = test_client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307

    def test_root_redirects_to_static_index(self, test_client):
        """Test that root redirects to /static/index.html."""
        # Arrange
        expected_location = "/static/index.html"

        # Act
        response = test_client.get("/", follow_redirects=False)

        # Assert
        assert response.headers["location"] == expected_location
