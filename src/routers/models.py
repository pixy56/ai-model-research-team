"""
API endpoints for Model operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db
from src.schemas.model import (
    ModelCreate,
    ModelUpdate,
    ModelResponse,
    ModelListResponse,
    SearchResponse,
)
from src.services.model_service import ModelService

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("", response_model=ModelListResponse)
def list_models(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    List all models with pagination.
    
    - **page**: Page number (1-indexed)
    - **page_size**: Number of items per page (1-100)
    """
    skip = (page - 1) * page_size
    result = ModelService.get_models(db, skip=skip, limit=page_size)
    return result


@router.get("/search", response_model=SearchResponse)
def search_models(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    Search models by name, lab, or tags.
    
    - **q**: Search query string
    - **page**: Page number (1-indexed)
    - **page_size**: Number of items per page (1-100)
    """
    skip = (page - 1) * page_size
    result = ModelService.search_models(db, query=q, skip=skip, limit=page_size)
    return result


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific model by ID.
    
    - **model_id**: The model ID
    """
    model = ModelService.get_model(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.post("", response_model=ModelResponse, status_code=201)
def create_model(
    model_data: ModelCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new model.
    
    All fields from the model schema are required except benchmarks and tags.
    """
    return ModelService.create_model(db, model_data)


@router.put("/{model_id}", response_model=ModelResponse)
def update_model(
    model_id: int,
    model_data: ModelUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing model.
    
    Only provided fields will be updated.
    """
    model = ModelService.update_model(db, model_id, model_data)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.delete("/{model_id}", status_code=204)
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a model.
    
    - **model_id**: The model ID to delete
    """
    success = ModelService.delete_model(db, model_id)
    if not success:
        raise HTTPException(status_code=404, detail="Model not found")
    return None
