"""
Pydantic schemas for the Model Database API.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List, Union
from datetime import datetime


class BenchmarkBase(BaseModel):
    """Base schema for Benchmark."""
    benchmark_name: str
    score: float
    metric: str = "score"


class BenchmarkCreate(BenchmarkBase):
    """Schema for creating a Benchmark."""
    pass


class BenchmarkResponse(BenchmarkBase):
    """Schema for Benchmark response."""
    id: int
    model_id: int

    class Config:
        from_attributes = True


class TagBase(BaseModel):
    """Base schema for Tag."""
    tag_name: str


class TagCreate(TagBase):
    """Schema for creating a Tag."""
    pass


class TagResponse(TagBase):
    """Schema for Tag response."""
    id: int
    model_id: int

    class Config:
        from_attributes = True


class ModelBase(BaseModel):
    """Base schema for Model."""
    name: str = Field(..., min_length=1, description="Model name, e.g., 'GPT-4'")
    lab: str = Field(..., min_length=1, description="Research lab or organization")
    release_date: str = Field(..., description="ISO 8601 date string (YYYY-MM-DD)")
    architecture: str = Field(..., description="Model architecture type")
    parameters: Union[float, str] = Field(..., description="Number of parameters in billions, or 'unknown'")
    context_window: Union[int, str] = Field(..., description="Context window size in tokens, or 'unknown'")
    paper_url: str = Field(..., description="URL to the research paper")
    announcement_url: str = Field(..., description="URL to the announcement blog post")
    benchmarks: Dict[str, float] = Field(default_factory=dict, description="Benchmark scores")
    tags: List[str] = Field(default_factory=list, description="Optional tags for categorization")

    @field_validator('architecture')
    @classmethod
    def validate_architecture(cls, v):
        """Validate architecture against allowed values."""
        allowed = ["dense-transformer", "moe", "ssm", "multimodal", "reasoning", "other"]
        if v not in allowed:
            raise ValueError(f"architecture must be one of: {', '.join(allowed)}")
        return v

    @field_validator('parameters')
    @classmethod
    def validate_parameters(cls, v):
        """Validate parameters - can be number or 'unknown'."""
        if isinstance(v, str) and v != "unknown":
            raise ValueError("parameters must be a number or 'unknown'")
        return str(v) if isinstance(v, (int, float)) else v

    @field_validator('context_window')
    @classmethod
    def validate_context_window(cls, v):
        """Validate context_window - can be number or 'unknown'."""
        if isinstance(v, str) and v != "unknown":
            raise ValueError("context_window must be a number or 'unknown'")
        return str(v) if isinstance(v, int) else v


class ModelCreate(ModelBase):
    """Schema for creating a Model."""
    pass


class ModelUpdate(BaseModel):
    """Schema for updating a Model - all fields optional."""
    name: Optional[str] = Field(None, min_length=1)
    lab: Optional[str] = Field(None, min_length=1)
    release_date: Optional[str] = None
    architecture: Optional[str] = None
    parameters: Optional[Union[float, str]] = None
    context_window: Optional[Union[int, str]] = None
    paper_url: Optional[str] = None
    announcement_url: Optional[str] = None
    benchmarks: Optional[Dict[str, float]] = None
    tags: Optional[List[str]] = None

    @field_validator('architecture')
    @classmethod
    def validate_architecture(cls, v):
        """Validate architecture against allowed values."""
        if v is None:
            return v
        allowed = ["dense-transformer", "moe", "ssm", "multimodal", "reasoning", "other"]
        if v not in allowed:
            raise ValueError(f"architecture must be one of: {', '.join(allowed)}")
        return v

    @field_validator('parameters')
    @classmethod
    def validate_parameters(cls, v):
        """Validate parameters - can be number or 'unknown'."""
        if v is None:
            return v
        if isinstance(v, str) and v != "unknown":
            raise ValueError("parameters must be a number or 'unknown'")
        return str(v) if isinstance(v, (int, float)) else v

    @field_validator('context_window')
    @classmethod
    def validate_context_window(cls, v):
        """Validate context_window - can be number or 'unknown'."""
        if v is None:
            return v
        if isinstance(v, str) and v != "unknown":
            raise ValueError("context_window must be a number or 'unknown'")
        return str(v) if isinstance(v, int) else v


class ModelResponse(BaseModel):
    """Schema for Model response - matches JSON schema format."""
    id: int
    name: str
    lab: str
    release_date: str
    architecture: str
    parameters: Union[float, str]
    context_window: Union[int, str]
    paper_url: str
    announcement_url: str
    benchmarks: Dict[str, float]
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModelListResponse(BaseModel):
    """Schema for paginated list of models."""
    items: List[ModelResponse]
    total: int
    page: int
    page_size: int
    pages: int


class SearchResponse(BaseModel):
    """Schema for search results."""
    items: List[ModelResponse]
    total: int
    query: str
