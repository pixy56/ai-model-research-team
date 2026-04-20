#!/bin/bash
# Startup script for the Model Database API

# Set Python path to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Start the FastAPI application with uvicorn
python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
