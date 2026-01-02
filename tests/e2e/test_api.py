"""End-to-end API tests for Nwassik.

These tests run against a deployed API and require:
- A deployed API (dev/staging/prod or custom stage)
- Valid AWS credentials with Cognito admin access
- Environment variables set in .env

Run with: pytest -m e2e
"""

from collections.abc import Generator

import httpx
import pytest

from tests.e2e.conftest import E2EUser

pytestmark = pytest.mark.e2e


class TestHealthCheck:
    """Health check endpoint tests."""

    def test_health_check_returns_ok(self, api_endpoint: str) -> None:
        """GET /health should return status ok."""
        response = httpx.get(f"{api_endpoint}/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Service is healthy"


class TestRequestsPublic:
    """Public requests endpoint tests."""

    def test_list_requests_returns_empty_or_list(self, api_endpoint: str) -> None:
        """GET /v0/requests should return a list with pagination."""
        response = httpx.get(f"{api_endpoint}/v0/requests")

        assert response.status_code == 200
        data = response.json()
        assert "requests" in data
        assert "pagination" in data
        assert isinstance(data["requests"], list)


class TestRequestsCRUD:
    """Authenticated requests CRUD tests."""

    @pytest.fixture(scope="class")
    def created_request_id(
        self,
        api_endpoint: str,
        auth_headers: dict,
    ) -> Generator[str, None, None]:
        """Create a request and return its ID for other tests."""
        payload = {
            "type": "buy_and_deliver",
            "title": "Test iPhone 16 Pro",
            "description": "Need iPhone 16 Pro from Paris",
            "dropoff_latitude": 36.8065,
            "dropoff_longitude": 10.1815,
        }

        response = httpx.post(
            f"{api_endpoint}/v0/requests",
            headers={**auth_headers, "Content-Type": "application/json"},
            json=payload,
        )

        assert response.status_code == 201, f"Failed to create request: {response.text}"
        data = response.json()
        assert "request_id" in data

        yield data["request_id"]

        # Cleanup: delete the request
        httpx.delete(
            f"{api_endpoint}/v0/requests/{data['request_id']}",
            headers=auth_headers,
        )

    def test_create_request(self, api_endpoint: str, auth_headers: dict) -> None:
        """POST /v0/requests should create a new request."""
        payload = {
            "type": "buy_and_deliver",
            "title": "Test Request Creation",
            "description": "Testing request creation",
            "dropoff_latitude": 36.8065,
            "dropoff_longitude": 10.1815,
        }

        response = httpx.post(
            f"{api_endpoint}/v0/requests",
            headers={**auth_headers, "Content-Type": "application/json"},
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()
        assert "request_id" in data
        assert data["message"] == "Request created successfully"

        # Cleanup
        httpx.delete(
            f"{api_endpoint}/v0/requests/{data['request_id']}",
            headers=auth_headers,
        )

    def test_get_request(self, api_endpoint: str, created_request_id: str) -> None:
        """GET /v0/requests/{id} should return the request."""
        response = httpx.get(f"{api_endpoint}/v0/requests/{created_request_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["request"]["id"] == created_request_id
        assert data["request"]["title"] == "Test iPhone 16 Pro"

    def test_update_request(
        self,
        api_endpoint: str,
        auth_headers: dict,
        created_request_id: str,
    ) -> None:
        """PATCH /v0/requests/{id} should update the request."""
        payload = {
            "title": "Updated: iPhone 16 Pro Max",
            "description": "Updated - need it urgently",
        }

        response = httpx.patch(
            f"{api_endpoint}/v0/requests/{created_request_id}",
            headers={**auth_headers, "Content-Type": "application/json"},
            json=payload,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Request updated successfully"

    def test_list_user_requests(
        self,
        api_endpoint: str,
        auth_headers: dict,
        test_user: E2EUser,
        created_request_id: str,
    ) -> None:
        """GET /v0/users/{id}/requests should return user's requests."""
        response = httpx.get(
            f"{api_endpoint}/v0/users/{test_user.user_id}/requests",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "requests" in data
        # Should contain the created request
        request_ids = [r["id"] for r in data["requests"]]
        assert created_request_id in request_ids


class TestFavoritesCRUD:
    """Authenticated favorites CRUD tests."""

    @pytest.fixture(scope="class")
    def request_for_favorite(
        self,
        api_endpoint: str,
        auth_headers: dict,
    ) -> Generator[str, None, None]:
        """Create a request to be favorited."""
        payload = {
            "type": "buy_and_deliver",
            "title": "Request for Favorite Test",
            "description": "This request will be favorited",
            "dropoff_latitude": 36.8065,
            "dropoff_longitude": 10.1815,
        }

        response = httpx.post(
            f"{api_endpoint}/v0/requests",
            headers={**auth_headers, "Content-Type": "application/json"},
            json=payload,
        )

        data = response.json()
        yield data["request_id"]

        # Cleanup
        httpx.delete(
            f"{api_endpoint}/v0/requests/{data['request_id']}",
            headers=auth_headers,
        )

    def test_create_favorite(
        self,
        api_endpoint: str,
        auth_headers: dict,
        request_for_favorite: str,
    ) -> None:
        """POST /v0/favorites should create a favorite."""
        response = httpx.post(
            f"{api_endpoint}/v0/favorites",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={"request_id": request_for_favorite},
        )

        assert response.status_code == 200
        data = response.json()
        assert "favorite_id" in data

        # Cleanup
        httpx.delete(
            f"{api_endpoint}/v0/favorites/{data['favorite_id']}",
            headers=auth_headers,
        )

    def test_list_favorites(self, api_endpoint: str, auth_headers: dict) -> None:
        """GET /v0/favorites should return user's favorites."""
        response = httpx.get(
            f"{api_endpoint}/v0/favorites",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "favorites" in data
        assert isinstance(data["favorites"], list)

    def test_favorite_lifecycle(
        self,
        api_endpoint: str,
        auth_headers: dict,
        request_for_favorite: str,
    ) -> None:
        """Test complete favorite lifecycle: create, list, delete."""
        # Create favorite
        create_response = httpx.post(
            f"{api_endpoint}/v0/favorites",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={"request_id": request_for_favorite},
        )
        assert create_response.status_code == 200
        favorite_id = create_response.json()["favorite_id"]

        # Verify it appears in list
        list_response = httpx.get(
            f"{api_endpoint}/v0/favorites",
            headers=auth_headers,
        )
        assert list_response.status_code == 200
        favorite_ids = [f["id"] for f in list_response.json()["favorites"]]
        assert favorite_id in favorite_ids

        # Delete favorite
        delete_response = httpx.delete(
            f"{api_endpoint}/v0/favorites/{favorite_id}",
            headers=auth_headers,
        )
        assert delete_response.status_code == 200

        # Verify it's gone
        list_response_after = httpx.get(
            f"{api_endpoint}/v0/favorites",
            headers=auth_headers,
        )
        favorite_ids_after = [f["id"] for f in list_response_after.json()["favorites"]]
        assert favorite_id not in favorite_ids_after


class TestRequestDelete:
    """Request deletion tests."""

    def test_delete_request(self, api_endpoint: str, auth_headers: dict) -> None:
        """DELETE /v0/requests/{id} should delete the request."""
        # First create a request
        payload = {
            "type": "buy_and_deliver",
            "title": "Request to Delete",
            "description": "This will be deleted",
            "dropoff_latitude": 36.8065,
            "dropoff_longitude": 10.1815,
        }

        create_response = httpx.post(
            f"{api_endpoint}/v0/requests",
            headers={**auth_headers, "Content-Type": "application/json"},
            json=payload,
        )
        request_id = create_response.json()["request_id"]

        # Delete it
        delete_response = httpx.delete(
            f"{api_endpoint}/v0/requests/{request_id}",
            headers=auth_headers,
        )
        assert delete_response.status_code == 204

        # Verify it's gone
        get_response = httpx.get(f"{api_endpoint}/v0/requests/{request_id}")
        assert get_response.status_code == 404


class TestUnauthorized:
    """Test unauthorized access to protected endpoints."""

    def test_create_request_without_auth_fails(self, api_endpoint: str) -> None:
        """POST /v0/requests without auth should fail."""
        payload = {
            "type": "buy_and_deliver",
            "title": "Unauthorized Request",
            "description": "Should fail",
            "dropoff_latitude": 36.8065,
            "dropoff_longitude": 10.1815,
        }

        response = httpx.post(
            f"{api_endpoint}/v0/requests",
            headers={"Content-Type": "application/json"},
            json=payload,
        )

        assert response.status_code == 401

    def test_list_favorites_without_auth_fails(self, api_endpoint: str) -> None:
        """GET /v0/favorites without auth should fail."""
        response = httpx.get(f"{api_endpoint}/v0/favorites")

        assert response.status_code == 401
