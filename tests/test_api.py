"""
Tests for the Model API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "AI Model Research Database API"
        assert "version" in data
        assert data["docs"] == "/docs"

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestCreateModel:
    """Tests for creating models."""

    def test_create_model_success(self, client: TestClient, sample_model_data):
        """Test creating a model with valid data."""
        response = client.post("/api/models", json=sample_model_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_model_data["name"]
        assert data["lab"] == sample_model_data["lab"]
        assert data["id"] is not None
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_model_with_unknown_params(self, client: TestClient, sample_model_data_unknown_params):
        """Test creating a model with unknown parameters."""
        response = client.post("/api/models", json=sample_model_data_unknown_params)
        assert response.status_code == 201
        data = response.json()
        assert data["parameters"] == "unknown"

    def test_create_model_missing_required_field(self, client: TestClient):
        """Test creating a model without required field fails."""
        invalid_data = {
            "name": "Test Model",
            "lab": "Test Lab",
            # missing release_date, architecture, etc.
        }
        response = client.post("/api/models", json=invalid_data)
        assert response.status_code == 422

    def test_create_model_invalid_architecture(self, client: TestClient, sample_model_data):
        """Test creating a model with invalid architecture fails."""
        invalid_data = {**sample_model_data, "architecture": "invalid-arch"}
        response = client.post("/api/models", json=invalid_data)
        assert response.status_code == 422


class TestGetModel:
    """Tests for getting models."""

    def test_get_model_success(self, client: TestClient, sample_model_data):
        """Test getting a model by ID."""
        # First create a model
        create_response = client.post("/api/models", json=sample_model_data)
        model_id = create_response.json()["id"]

        # Then get it
        response = client.get(f"/api/models/{model_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_model_data["name"]
        assert data["benchmarks"] == sample_model_data["benchmarks"]
        assert data["tags"] == sample_model_data["tags"]

    def test_get_model_not_found(self, client: TestClient):
        """Test getting a non-existent model returns 404."""
        response = client.get("/api/models/999")
        assert response.status_code == 404


class TestListModels:
    """Tests for listing models."""

    def test_list_models_empty(self, client: TestClient):
        """Test listing models when none exist."""
        response = client.get("/api/models")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_models_with_pagination(self, client: TestClient, sample_model_data):
        """Test listing models with pagination."""
        # Create multiple models
        for i in range(5):
            data = {**sample_model_data, "name": f"Model {i}"}
            client.post("/api/models", json=data)

        # Get first page
        response = client.get("/api/models?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["pages"] == 3

    def test_list_models_default_pagination(self, client: TestClient, sample_model_data):
        """Test listing models with default pagination."""
        # Create a model
        client.post("/api/models", json=sample_model_data)

        response = client.get("/api/models")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert "pages" in data


class TestUpdateModel:
    """Tests for updating models."""

    def test_update_model_success(self, client: TestClient, sample_model_data):
        """Test updating a model."""
        # First create a model
        create_response = client.post("/api/models", json=sample_model_data)
        model_id = create_response.json()["id"]

        # Update it
        update_data = {"name": "Updated Model Name"}
        response = client.put(f"/api/models/{model_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Model Name"
        assert data["lab"] == sample_model_data["lab"]  # Unchanged

    def test_update_model_not_found(self, client: TestClient):
        """Test updating a non-existent model returns 404."""
        response = client.put("/api/models/999", json={"name": "New Name"})
        assert response.status_code == 404

    def test_update_model_invalid_architecture(self, client: TestClient, sample_model_data):
        """Test updating with invalid architecture fails."""
        # First create a model
        create_response = client.post("/api/models", json=sample_model_data)
        model_id = create_response.json()["id"]

        # Try to update with invalid architecture
        response = client.put(f"/api/models/{model_id}", json={"architecture": "invalid"})
        assert response.status_code == 422


class TestDeleteModel:
    """Tests for deleting models."""

    def test_delete_model_success(self, client: TestClient, sample_model_data):
        """Test deleting a model."""
        # First create a model
        create_response = client.post("/api/models", json=sample_model_data)
        model_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/api/models/{model_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/api/models/{model_id}")
        assert get_response.status_code == 404

    def test_delete_model_not_found(self, client: TestClient):
        """Test deleting a non-existent model returns 404."""
        response = client.delete("/api/models/999")
        assert response.status_code == 404


class TestSearchModels:
    """Tests for searching models."""

    def test_search_by_name(self, client: TestClient, sample_model_data):
        """Test searching models by name."""
        # Create a model
        client.post("/api/models", json=sample_model_data)

        # Search for it
        response = client.get(f"/api/models/search?q={sample_model_data['name']}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any(m["name"] == sample_model_data["name"] for m in data["items"])

    def test_search_by_lab(self, client: TestClient, sample_model_data):
        """Test searching models by lab."""
        # Create a model
        client.post("/api/models", json=sample_model_data)

        # Search by lab
        response = client.get(f"/api/models/search?q={sample_model_data['lab']}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    def test_search_by_tag(self, client: TestClient, sample_model_data):
        """Test searching models by tag."""
        # Create a model with tags
        client.post("/api/models", json=sample_model_data)

        # Search by first tag
        tag = sample_model_data["tags"][0]
        response = client.get(f"/api/models/search?q={tag}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    def test_search_no_results(self, client: TestClient):
        """Test searching with no matches."""
        response = client.get("/api/models/search?q=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_search_empty_query(self, client: TestClient):
        """Test searching with empty query fails."""
        response = client.get("/api/models/search?q=")
        assert response.status_code == 422
