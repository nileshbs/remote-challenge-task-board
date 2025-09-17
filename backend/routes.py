"""
API routes for the Task Manager application.

This module defines all API endpoints, following the Single Responsibility Principle (SRP)
and using dependency injection for clean separation of concerns.
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from models import (
    LoginRequest, LoginResponse, TaskRequest, TaskUpdateRequest,
    TaskResponse, TaskListResponse, DeleteResponse
)
from auth_service import auth_service, get_current_user, AuthenticationError
from task_service import task_service, TaskError
from config import settings

logger = logging.getLogger(__name__)

# Create router instances
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])
tasks_router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@auth_router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest) -> LoginResponse:
    """
    Authenticate user credentials and return access token.
    
    Args:
        login_request: User credentials
        
    Returns:
        LoginResponse with user data and access token
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        user_data = auth_service.authenticate_user(
            login_request.username, 
            login_request.password
        )
        
        if user_data is None:
            raise HTTPException(
                status_code=401,
                detail=settings.ErrorMessages.INVALID_CREDENTIALS
            )
        
        return LoginResponse(
            access_token=user_data.access_token,
            user_id=user_data.user_id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Authentication service error"
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@tasks_router.get("", response_model=TaskListResponse)
async def get_user_tasks(
    current_user = Depends(get_current_user)
) -> TaskListResponse:
    """
    Get all tasks for the authenticated user.
    
    Args:
        current_user: The authenticated user (injected dependency)
        
    Returns:
        TaskListResponse with user's tasks
        
    Raises:
        HTTPException: If tasks cannot be retrieved
    """
    try:
        tasks = task_service.get_user_tasks(current_user.user_id)
        
        return TaskListResponse(
            tasks=tasks,
            total=len(tasks)
        )
        
    except TaskError as e:
        logger.error(f"Task service error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error retrieving tasks: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@tasks_router.post("", response_model=TaskResponse)
async def create_task(
    task_request: TaskRequest,
    current_user = Depends(get_current_user)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.
    
    Args:
        task_request: Task creation data
        current_user: The authenticated user (injected dependency)
        
    Returns:
        TaskResponse for the created task
        
    Raises:
        HTTPException: If task cannot be created
    """
    try:
        task_response = task_service.create_task(task_request, current_user)
        return task_response
        
    except TaskError as e:
        logger.error(f"Task service error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating task: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@tasks_router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdateRequest,
    current_user = Depends(get_current_user)
) -> TaskResponse:
    """
    Update an existing task for the authenticated user.
    
    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        current_user: The authenticated user (injected dependency)
        
    Returns:
        TaskResponse for the updated task
        
    Raises:
        HTTPException: If task cannot be updated
    """
    try:
        task_response = task_service.update_task(task_id, task_update, current_user)
        return task_response
        
    except TaskError as e:
        error_message = str(e)
        if error_message == settings.ErrorMessages.TASK_NOT_FOUND:
            raise HTTPException(status_code=404, detail=error_message)
        elif error_message == settings.ErrorMessages.NO_UPDATE_FIELDS:
            raise HTTPException(status_code=400, detail=error_message)
        else:
            raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        logger.error(f"Unexpected error updating task: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@tasks_router.delete("/{task_id}", response_model=DeleteResponse)
async def delete_task(
    task_id: str,
    current_user = Depends(get_current_user)
) -> DeleteResponse:
    """
    Delete a task for the authenticated user.
    
    Args:
        task_id: The ID of the task to delete
        current_user: The authenticated user (injected dependency)
        
    Returns:
        DeleteResponse with success message
        
    Raises:
        HTTPException: If task cannot be deleted
    """
    try:
        success = task_service.delete_task(task_id, current_user)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=settings.ErrorMessages.TASK_NOT_FOUND
            )
        
        return DeleteResponse(
            message="Task deleted successfully",
            task_id=task_id
        )
        
    except TaskError as e:
        error_message = str(e)
        if error_message == settings.ErrorMessages.TASK_NOT_FOUND:
            raise HTTPException(status_code=404, detail=error_message)
        else:
            raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        logger.error(f"Unexpected error deleting task: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
