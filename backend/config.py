"""
Configuration module for the Task Manager API.

This module contains all configuration settings, constants, and environment variables.
Following the Single Responsibility Principle (SRP) from SOLID principles.
"""

import os
from pathlib import Path
from typing import List


class Settings:
    """Application settings and configuration."""
    
    # API Configuration
    API_TITLE: str = "Task Manager API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A modern task management API with authentication"
    
    # Server Configuration
    HOST: str = "10.0.0.8"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://10.0.0.8:3000",
        "http://10.0.0.8:5173", 
        "http://10.0.0.8:8080",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080"
    ]
    
    # Database Configuration
    DATABASE_DIR: Path = Path(__file__).parent.parent / "database"
    USERS_FILE: Path = DATABASE_DIR / "users.json"
    TASKS_FILE: Path = DATABASE_DIR / "tasks.json"
    
    # Security Configuration
    TOKEN_HEADER: str = "Authorization"
    TOKEN_PREFIX: str = "Bearer "
    
    # Task Configuration
    DEFAULT_TASK_STATUS: str = "To Do"
    VALID_TASK_STATUSES: List[str] = ["To Do", "In Progress", "Completed"]
    MAX_TASK_TITLE_LENGTH: int = 200
    MAX_TASK_DETAILS_LENGTH: int = 1000
    
    # Error Messages
    class ErrorMessages:
        """Centralized error messages."""
        USER_NOT_FOUND = "User not found"
        INVALID_CREDENTIALS = "Invalid username or password"
        TOKEN_MISSING = "Authorization header missing"
        TOKEN_INVALID_FORMAT = "Invalid authorization format"
        TOKEN_INVALID = "Invalid or expired token"
        TASK_NOT_FOUND = "Task not found or access denied"
        NO_UPDATE_FIELDS = "No fields provided for update"
        DATABASE_NOT_FOUND = "Database file not found"
        DATABASE_INVALID_FORMAT = "Invalid database format"
        SAVE_FAILED = "Failed to save data"
        INVALID_TASK_STATUS = "Invalid task status"
        TASK_TITLE_TOO_LONG = f"Task title must be less than 200 characters"
        TASK_DETAILS_TOO_LONG = f"Task details must be less than 1000 characters"


# Global settings instance
settings = Settings()
