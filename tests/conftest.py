"""
Pytest configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app

# Create test database in memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with fresh database."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_model_data():
    """Sample model data for testing."""
    return {
        "name": "Test Model",
        "lab": "Test Lab",
        "release_date": "2024-01-01",
        "architecture": "dense-transformer",
        "parameters": 7.0,
        "context_window": 4096,
        "paper_url": "https://arxiv.org/abs/2401.00001",
        "announcement_url": "https://example.com/announcement",
        "benchmarks": {"mmlu": 85.5, "humaneval": 70.0},
        "tags": ["test", "example"],
    }


@pytest.fixture
def sample_model_data_unknown_params():
    """Sample model data with unknown parameters."""
    return {
        "name": "GPT-4",
        "lab": "OpenAI",
        "release_date": "2023-03-14",
        "architecture": "dense-transformer",
        "parameters": "unknown",
        "context_window": 8192,
        "paper_url": "https://arxiv.org/abs/2303.08774",
        "announcement_url": "https://openai.com/blog/gpt-4",
        "benchmarks": {"mmlu": 86.4, "humaneval": 67.0},
        "tags": ["multimodal", "reasoning"],
    }
