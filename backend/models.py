"""
Pydantic models for request/response schemas.

This module defines all data models used in the API, following the
Single Responsibility Principle (SRP) and providing clear data contracts.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from config import settings


class LoginRequest(BaseModel):
    """Request model for user authentication."""
    username: str = Field(..., min_length=1, max_length=100, description="Username")
    password: str = Field(..., min_length=1, max_length=100, description="Password")


class LoginResponse(BaseModel):
    """Response model for successful authentication."""
    access_token: str = Field(..., description="JWT access token")
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., description="Username")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")


class TaskRequest(BaseModel):
    """Request model for creating a new task."""
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=settings.MAX_TASK_TITLE_LENGTH,
        description="Task title"
    )
    details: str = Field(
        default="", 
        max_length=settings.MAX_TASK_DETAILS_LENGTH,
        description="Task details"
    )
    due_date: date = Field(..., description="Task due date")
    status: str = Field(
        default=settings.DEFAULT_TASK_STATUS,
        description="Task status"
    )
    
    @validator('status')
    def validate_status(cls, v):
        """Validate task status."""
        if v not in settings.VALID_TASK_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(settings.VALID_TASK_STATUSES)}")
        return v
    
    @validator('title')
    def validate_title(cls, v):
        """Validate and clean task title."""
        return v.strip()
    
    @validator('details')
    def validate_details(cls, v):
        """Validate and clean task details."""
        return v.strip()


class TaskUpdateRequest(BaseModel):
    """Request model for updating an existing task."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=settings.MAX_TASK_TITLE_LENGTH,
        description="Updated task title"
    )
    details: Optional[str] = Field(
        None,
        max_length=settings.MAX_TASK_DETAILS_LENGTH,
        description="Updated task details"
    )
    due_date: Optional[date] = Field(None, description="Updated due date")
    status: Optional[str] = Field(None, description="Updated task status")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate task status if provided."""
        if v is not None and v not in settings.VALID_TASK_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(settings.VALID_TASK_STATUSES)}")
        return v
    
    @validator('title')
    def validate_title(cls, v):
        """Validate and clean task title if provided."""
        if v is not None:
            return v.strip()
        return v
    
    @validator('details')
    def validate_details(cls, v):
        """Validate and clean task details if provided."""
        if v is not None:
            return v.strip()
        return v


class TaskResponse(BaseModel):
    """Response model for task data."""
    task_id: str = Field(..., description="Unique task identifier")
    userId: str = Field(..., description="User ID who owns the task")
    title: str = Field(..., description="Task title")
    details: str = Field(..., description="Task details")
    due_date: str = Field(..., description="Task due date")
    status: str = Field(..., description="Task status")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            date: lambda v: v.isoformat()
        }


class TaskListResponse(BaseModel):
    """Response model for a list of tasks."""
    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    
    @validator('total', always=True)
    def set_total(cls, v, values):
        """Set total count based on tasks list length."""
        if 'tasks' in values:
            return len(values['tasks'])
        return v


class DeleteResponse(BaseModel):
    """Response model for successful deletion."""
    message: str = Field(..., description="Success message")
    task_id: str = Field(..., description="ID of deleted task")


class ErrorResponse(BaseModel):
    """Response model for error messages."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")


class UserInfo(BaseModel):
    """Internal model for user information."""
    user_id: str
    username: str
    first_name: str
    last_name: str
    access_token: Optional[str] = None
