#!/usr/bin/env python3
"""
Server runner script for the Task Manager API.

This script provides a clean entry point for running the application
with proper configuration and error handling.
"""

import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Server error: {e}")
        sys.exit(1)
