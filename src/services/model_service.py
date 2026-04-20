"""
Business logic for Model operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from src.models.model import Model, Benchmark, Tag
from src.schemas.model import ModelCreate, ModelUpdate


def _benchmarks_to_dict(benchmarks: List[Benchmark]) -> Dict[str, float]:
    """Convert list of Benchmark objects to dict."""
    return {b.benchmark_name: b.score for b in benchmarks}


def _tags_to_list(tags: List[Tag]) -> List[str]:
    """Convert list of Tag objects to list of strings."""
    return [t.tag_name for t in tags]


def _model_to_dict(model: Model) -> Dict[str, Any]:
    """Convert Model ORM object to dict matching response schema."""
    return {
        "id": model.id,
        "name": model.name,
        "lab": model.lab,
        "release_date": model.release_date,
        "architecture": model.architecture,
        "parameters": model.parameters if model.parameters == "unknown" else float(model.parameters),
        "context_window": model.context_window if model.context_window == "unknown" else int(model.context_window),
        "paper_url": model.paper_url,
        "announcement_url": model.announcement_url,
        "benchmarks": _benchmarks_to_dict(model.benchmarks),
        "tags": _tags_to_list(model.tags),
        "created_at": model.created_at,
        "updated_at": model.updated_at,
    }


class ModelService:
    """Service class for Model operations."""

    @staticmethod
    def get_models(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get paginated list of models."""
        query = db.query(Model)
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        page = (skip // limit) + 1 if limit > 0 else 1
        
        return {
            "items": [_model_to_dict(m) for m in models],
            "total": total,
            "page": page,
            "page_size": limit,
            "pages": pages,
        }

    @staticmethod
    def get_model(db: Session, model_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific model by ID."""
        model = db.query(Model).filter(Model.id == model_id).first()
        if model:
            return _model_to_dict(model)
        return None

    @staticmethod
    def create_model(db: Session, model_data: ModelCreate) -> Dict[str, Any]:
        """Create a new model."""
        # Create model
        db_model = Model(
            name=model_data.name,
            lab=model_data.lab,
            release_date=model_data.release_date,
            architecture=model_data.architecture,
            parameters=str(model_data.parameters),
            context_window=str(model_data.context_window),
            paper_url=model_data.paper_url,
            announcement_url=model_data.announcement_url,
        )
        db.add(db_model)
        db.flush()  # Flush to get the ID

        # Create benchmarks
        for name, score in model_data.benchmarks.items():
            db_benchmark = Benchmark(
                model_id=db_model.id,
                benchmark_name=name,
                score=score,
            )
            db.add(db_benchmark)

        # Create tags
        for tag_name in model_data.tags:
            db_tag = Tag(
                model_id=db_model.id,
                tag_name=tag_name,
            )
            db.add(db_tag)

        db.commit()
        db.refresh(db_model)
        return _model_to_dict(db_model)

    @staticmethod
    def update_model(
        db: Session,
        model_id: int,
        model_data: ModelUpdate
    ) -> Optional[Dict[str, Any]]:
        """Update an existing model."""
        model = db.query(Model).filter(Model.id == model_id).first()
        if not model:
            return None

        # Update model fields
        update_data = model_data.model_dump(exclude_unset=True)
        
        # Handle benchmarks separately
        if "benchmarks" in update_data:
            benchmarks_data = update_data.pop("benchmarks")
            # Delete existing benchmarks
            db.query(Benchmark).filter(Benchmark.model_id == model_id).delete()
            # Create new benchmarks
            for name, score in benchmarks_data.items():
                db_benchmark = Benchmark(
                    model_id=model_id,
                    benchmark_name=name,
                    score=score,
                )
                db.add(db_benchmark)

        # Handle tags separately
        if "tags" in update_data:
            tags_data = update_data.pop("tags")
            # Delete existing tags
            db.query(Tag).filter(Tag.model_id == model_id).delete()
            # Create new tags
            for tag_name in tags_data:
                db_tag = Tag(
                    model_id=model_id,
                    tag_name=tag_name,
                )
                db.add(db_tag)

        # Update remaining model fields
        for field, value in update_data.items():
            if field in ["parameters", "context_window"] and value is not None:
                value = str(value)
            setattr(model, field, value)

        db.commit()
        db.refresh(model)
        return _model_to_dict(model)

    @staticmethod
    def delete_model(db: Session, model_id: int) -> bool:
        """Delete a model."""
        model = db.query(Model).filter(Model.id == model_id).first()
        if not model:
            return False
        
        db.delete(model)
        db.commit()
        return True

    @staticmethod
    def search_models(
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Search models by name, lab, or tags."""
        search_filter = or_(
            Model.name.ilike(f"%{query}%"),
            Model.lab.ilike(f"%{query}%"),
        )
        
        # Also search in tags
        tag_subquery = db.query(Tag.model_id).filter(
            Tag.tag_name.ilike(f"%{query}%")
        ).subquery()
        
        combined_filter = or_(
            search_filter,
            Model.id.in_(tag_subquery)
        )
        
        query_obj = db.query(Model).filter(combined_filter)
        total = query_obj.count()
        models = query_obj.offset(skip).limit(limit).all()
        
        return {
            "items": [_model_to_dict(m) for m in models],
            "total": total,
            "query": query,
        }
