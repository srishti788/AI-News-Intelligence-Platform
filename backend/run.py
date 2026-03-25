#!/usr/bin/env python
"""Simple script to run the FastAPI application"""
import sys
import os
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    try:
        import uvicorn
        from app.main import app
        
        print("Starting FastAPI server on http://0.0.0.0:8000")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except ImportError as e:
        print(f"Import Error: {e}")
        print(f"Python Path: {sys.path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
