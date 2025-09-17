"""
Task service for managing task operations.

This module handles all task-related business logic, following the
Single Responsibility Principle (SRP) and providing a clean interface.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import date

from models import TaskRequest, TaskUpdateRequest, TaskResponse, UserInfo
from database_service import DatabaseServiceFactory, DatabaseError
from config import settings

logger = logging.getLogger(__name__)


class TaskError(Exception):
    """Custom exception for task operations."""
    pass


class TaskService:
    """Service class for handling task operations."""
    
    def __init__(self):
        """Initialize the task service."""
        self.tasks_db = DatabaseServiceFactory.create_tasks_service()
    
    def get_user_tasks(self, user_id: str) -> List[TaskResponse]:
        """
        Get all tasks for a specific user.
        
        Args:
            user_id: The user ID to get tasks for
            
        Returns:
            List of TaskResponse objects
            
        Raises:
            TaskError: If tasks cannot be retrieved
        """
        try:
            tasks = self.tasks_db.find_by_field('userId', user_id)
            
            task_responses = []
            for task in tasks:
                task_response = TaskResponse(
                    task_id=task.get('task_id'),
                    userId=task.get('userId'),
                    title=task.get('title'),
                    details=task.get('details'),
                    due_date=task.get('due_date'),
                    status=task.get('status')
                )
                task_responses.append(task_response)
            
            logger.info(f"Retrieved {len(task_responses)} tasks for user {user_id}")
            return task_responses
            
        except DatabaseError as e:
            logger.error(f"Database error retrieving tasks for user {user_id}: {e}")
            raise TaskError("Failed to retrieve tasks")
        except Exception as e:
            logger.error(f"Unexpected error retrieving tasks for user {user_id}: {e}")
            raise TaskError("Failed to retrieve tasks")
    
    def create_task(self, task_request: TaskRequest, user: UserInfo) -> TaskResponse:
        """
        Create a new task for a user.
        
        Args:
            task_request: The task creation request
            user: The user creating the task
            
        Returns:
            TaskResponse object for the created task
            
        Raises:
            TaskError: If task cannot be created
        """
        try:
            # Generate new task ID
            new_task_id = self.tasks_db.get_next_id('task_id')
            
            # Create task data
            task_data = {
                'task_id': new_task_id,
                'userId': user.user_id,
                'title': task_request.title,
                'details': task_request.details,
                'due_date': task_request.due_date.isoformat(),
                'status': task_request.status
            }
            
            # Add to database
            self.tasks_db.add_item(task_data)
            
            # Create response
            task_response = TaskResponse(
                task_id=task_data['task_id'],
                userId=task_data['userId'],
                title=task_data['title'],
                details=task_data['details'],
                due_date=task_data['due_date'],
                status=task_data['status']
            )
            
            logger.info(f"Created task {new_task_id} for user {user.user_id}")
            return task_response
            
        except DatabaseError as e:
            logger.error(f"Database error creating task for user {user.user_id}: {e}")
            raise TaskError("Failed to create task")
        except Exception as e:
            logger.error(f"Unexpected error creating task for user {user.user_id}: {e}")
            raise TaskError("Failed to create task")
    
    def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific task by ID, ensuring it belongs to the user.
        
        Args:
            task_id: The task ID to retrieve
            user_id: The user ID to verify ownership
            
        Returns:
            Task data if found and owned by user, None otherwise
        """
        try:
            task = self.tasks_db.find_by_id(task_id)
            if task and task.get('userId') == user_id:
                return task
            return None
            
        except DatabaseError as e:
            logger.error(f"Database error retrieving task {task_id}: {e}")
            raise TaskError("Failed to retrieve task")
    
    def update_task(self, task_id: str, task_update: TaskUpdateRequest, user: UserInfo) -> TaskResponse:
        """
        Update an existing task.
        
        Args:
            task_id: The task ID to update
            task_update: The update request data
            user: The user making the update
            
        Returns:
            TaskResponse object for the updated task
            
        Raises:
            TaskError: If task cannot be updated
        """
        try:
            # Check if task exists and belongs to user
            existing_task = self.get_task_by_id(task_id, user.user_id)
            if not existing_task:
                raise TaskError(settings.ErrorMessages.TASK_NOT_FOUND)
            
            # Prepare update data (only include non-None values)
            update_data = {}
            if task_update.title is not None:
                update_data['title'] = task_update.title
            if task_update.details is not None:
                update_data['details'] = task_update.details
            if task_update.due_date is not None:
                update_data['due_date'] = task_update.due_date.isoformat()
            if task_update.status is not None:
                update_data['status'] = task_update.status
            
            # Check if there's anything to update
            if not update_data:
                raise TaskError(settings.ErrorMessages.NO_UPDATE_FIELDS)
            
            # Update the task
            success = self.tasks_db.update_item(task_id, update_data)
            if not success:
                raise TaskError("Failed to update task")
            
            # Get the updated task
            updated_task = self.get_task_by_id(task_id, user.user_id)
            
            # Create response
            task_response = TaskResponse(
                task_id=updated_task['task_id'],
                userId=updated_task['userId'],
                title=updated_task['title'],
                details=updated_task['details'],
                due_date=updated_task['due_date'],
                status=updated_task['status']
            )
            
            logger.info(f"Updated task {task_id} for user {user.user_id}")
            return task_response
            
        except TaskError:
            # Re-raise task errors
            raise
        except DatabaseError as e:
            logger.error(f"Database error updating task {task_id}: {e}")
            raise TaskError("Failed to update task")
        except Exception as e:
            logger.error(f"Unexpected error updating task {task_id}: {e}")
            raise TaskError("Failed to update task")
    
    def delete_task(self, task_id: str, user: UserInfo) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: The task ID to delete
            user: The user making the deletion
            
        Returns:
            True if task was deleted, False if not found
            
        Raises:
            TaskError: If task cannot be deleted
        """
        try:
            # Check if task exists and belongs to user
            existing_task = self.get_task_by_id(task_id, user.user_id)
            if not existing_task:
                raise TaskError(settings.ErrorMessages.TASK_NOT_FOUND)
            
            # Remove the task
            success = self.tasks_db.remove_item(task_id)
            if not success:
                raise TaskError("Failed to delete task")
            
            logger.info(f"Deleted task {task_id} for user {user.user_id}")
            return True
            
        except TaskError:
            # Re-raise task errors
            raise
        except DatabaseError as e:
            logger.error(f"Database error deleting task {task_id}: {e}")
            raise TaskError("Failed to delete task")
        except Exception as e:
            logger.error(f"Unexpected error deleting task {task_id}: {e}")
            raise TaskError("Failed to delete task")
    
    def validate_task_ownership(self, task_id: str, user_id: str) -> bool:
        """
        Validate that a task belongs to a specific user.
        
        Args:
            task_id: The task ID to validate
            user_id: The user ID to check ownership against
            
        Returns:
            True if user owns the task, False otherwise
        """
        try:
            task = self.get_task_by_id(task_id, user_id)
            return task is not None
        except TaskError:
            return False


# Global task service instance
task_service = TaskService()
