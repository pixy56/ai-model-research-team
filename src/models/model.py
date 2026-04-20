"""
SQLAlchemy models for the Model Database.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base


class Model(Base):
    """AI Model entity."""
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    lab = Column(String, nullable=False, index=True)
    release_date = Column(String, nullable=False)  # ISO 8601 date string
    architecture = Column(String, nullable=False)
    parameters = Column(String, nullable=False)  # Store as string to handle "unknown"
    context_window = Column(String, nullable=False)  # Store as string to handle "unknown"
    paper_url = Column(String, nullable=False)
    announcement_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    benchmarks = relationship("Benchmark", back_populates="model", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="model", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Model(id={self.id}, name='{self.name}', lab='{self.lab}')>"


class Benchmark(Base):
    """Benchmark score for a model."""
    __tablename__ = "benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    benchmark_name = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=False)
    metric = Column(String, default="score")

    # Relationships
    model = relationship("Model", back_populates="benchmarks")

    def __repr__(self):
        return f"<Benchmark(id={self.id}, name='{self.benchmark_name}', score={self.score})>"


class Tag(Base):
    """Tag for categorizing models."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    tag_name = Column(String, nullable=False, index=True)

    # Relationships
    model = relationship("Model", back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.tag_name}')>"
