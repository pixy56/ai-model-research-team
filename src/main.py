"""
Main FastAPI application for the Model Database API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import init_db
from src.routers import models

# Create FastAPI app
app = FastAPI(
    title="AI Model Research Database",
    description="API for managing AI model metadata",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(models.router)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "AI Model Research Database API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
