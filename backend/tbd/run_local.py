#!/usr/bin/env python3
"""
Local development server for FastAPI backend.
Run this script to start the backend server locally.
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting FastAPI backend server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation available at: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="10.0.0.8",
        port=8000,
        reload=True,
        log_level="info"
    )
