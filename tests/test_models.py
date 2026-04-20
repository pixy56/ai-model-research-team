"""
Tests for Model service layer.
"""

import pytest
from sqlalchemy.orm import Session

from src.services.model_service import ModelService
from src.schemas.model import ModelCreate, ModelUpdate


class TestModelService:
    """Tests for ModelService class."""

    def test_create_model(self, db: Session, sample_model_data):
        """Test creating a model through service."""
        model_create = ModelCreate(**sample_model_data)
        result = ModelService.create_model(db, model_create)
        
        assert result["name"] == sample_model_data["name"]
        assert result["lab"] == sample_model_data["lab"]
        assert result["id"] is not None
        assert result["benchmarks"] == sample_model_data["benchmarks"]
        assert result["tags"] == sample_model_data["tags"]

    def test_get_model(self, db: Session, sample_model_data):
        """Test getting a model by ID."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        created = ModelService.create_model(db, model_create)
        
        # Get it
        result = ModelService.get_model(db, created["id"])
        assert result is not None
        assert result["name"] == sample_model_data["name"]

    def test_get_model_not_found(self, db: Session):
        """Test getting non-existent model returns None."""
        result = ModelService.get_model(db, 999)
        assert result is None

    def test_get_models_pagination(self, db: Session, sample_model_data):
        """Test getting models with pagination."""
        # Create multiple models
        for i in range(5):
            data = {**sample_model_data, "name": f"Model {i}"}
            model_create = ModelCreate(**data)
            ModelService.create_model(db, model_create)
        
        # Get first page
        result = ModelService.get_models(db, skip=0, limit=2)
        assert result["total"] == 5
        assert len(result["items"]) == 2
        assert result["pages"] == 3

    def test_update_model(self, db: Session, sample_model_data):
        """Test updating a model."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        created = ModelService.create_model(db, model_create)
        
        # Update it
        update_data = ModelUpdate(name="Updated Name")
        result = ModelService.update_model(db, created["id"], update_data)
        
        assert result is not None
        assert result["name"] == "Updated Name"
        assert result["lab"] == sample_model_data["lab"]  # Unchanged

    def test_update_model_not_found(self, db: Session):
        """Test updating non-existent model returns None."""
        update_data = ModelUpdate(name="New Name")
        result = ModelService.update_model(db, 999, update_data)
        assert result is None

    def test_update_model_benchmarks(self, db: Session, sample_model_data):
        """Test updating model benchmarks replaces all."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        created = ModelService.create_model(db, model_create)
        
        # Update benchmarks
        update_data = ModelUpdate(benchmarks={"new_benchmark": 95.0})
        result = ModelService.update_model(db, created["id"], update_data)
        
        assert result["benchmarks"] == {"new_benchmark": 95.0}

    def test_update_model_tags(self, db: Session, sample_model_data):
        """Test updating model tags replaces all."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        created = ModelService.create_model(db, model_create)
        
        # Update tags
        update_data = ModelUpdate(tags=["new_tag"])
        result = ModelService.update_model(db, created["id"], update_data)
        
        assert result["tags"] == ["new_tag"]

    def test_delete_model(self, db: Session, sample_model_data):
        """Test deleting a model."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        created = ModelService.create_model(db, model_create)
        
        # Delete it
        success = ModelService.delete_model(db, created["id"])
        assert success is True
        
        # Verify it's gone
        result = ModelService.get_model(db, created["id"])
        assert result is None

    def test_delete_model_not_found(self, db: Session):
        """Test deleting non-existent model returns False."""
        success = ModelService.delete_model(db, 999)
        assert success is False

    def test_search_models_by_name(self, db: Session, sample_model_data):
        """Test searching models by name."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        ModelService.create_model(db, model_create)
        
        # Search
        result = ModelService.search_models(db, query=sample_model_data["name"])
        assert result["total"] >= 1
        assert any(m["name"] == sample_model_data["name"] for m in result["items"])

    def test_search_models_by_lab(self, db: Session, sample_model_data):
        """Test searching models by lab."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        ModelService.create_model(db, model_create)
        
        # Search
        result = ModelService.search_models(db, query=sample_model_data["lab"])
        assert result["total"] >= 1

    def test_search_models_by_tag(self, db: Session, sample_model_data):
        """Test searching models by tag."""
        # Create model
        model_create = ModelCreate(**sample_model_data)
        ModelService.create_model(db, model_create)
        
        # Search by tag
        tag = sample_model_data["tags"][0]
        result = ModelService.search_models(db, query=tag)
        assert result["total"] >= 1

    def test_search_models_no_results(self, db: Session):
        """Test searching with no matches."""
        result = ModelService.search_models(db, query="nonexistent")
        assert result["total"] == 0
        assert result["items"] == []

    def test_model_with_unknown_params(self, db: Session, sample_model_data_unknown_params):
        """Test creating model with unknown parameters."""
        model_create = ModelCreate(**sample_model_data_unknown_params)
        result = ModelService.create_model(db, model_create)
        
        assert result["parameters"] == "unknown"
        assert result["context_window"] == 8192
