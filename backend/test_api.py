"""
Comprehensive test suite for the Task Manager API.

This module contains tests for all API endpoints, following best practices
for testing FastAPI applications.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app import app
from models import UserInfo

# Create test client
client = TestClient(app)


class TestAuthentication:
    """Test cases for authentication endpoints."""
    
    def test_login_success(self):
        """Test successful user login."""
        with patch('auth_service.auth_service.authenticate_user') as mock_auth:
            mock_auth.return_value = UserInfo(
                user_id="A124242",
                username="johndoe",
                first_name="John",
                last_name="Doe",
                access_token="test_token"
            )
            
            response = client.post(
                "/api/auth/login",
                json={"username": "johndoe", "password": "password123"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "johndoe"
            assert data["user_id"] == "A124242"
            assert "access_token" in data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        with patch('auth_service.auth_service.authenticate_user') as mock_auth:
            mock_auth.return_value = None
            
            response = client.post(
                "/api/auth/login",
                json={"username": "invalid", "password": "wrong"}
            )
            
            assert response.status_code == 401
            assert "Invalid username or password" in response.json()["detail"]
    
    def test_login_missing_fields(self):
        """Test login with missing required fields."""
        response = client.post(
            "/api/auth/login",
            json={"username": "johndoe"}
        )
        
        assert response.status_code == 422  # Validation error


class TestTasks:
    """Test cases for task management endpoints."""
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user."""
        return UserInfo(
            user_id="A124242",
            username="johndoe",
            first_name="John",
            last_name="Doe"
        )
    
    @pytest.fixture
    def auth_headers(self):
        """Authentication headers for requests."""
        return {"Authorization": "Bearer test_token"}
    
    def test_get_tasks_success(self, mock_user, auth_headers):
        """Test successful task retrieval."""
        with patch('auth_service.get_current_user') as mock_get_user, \
             patch('task_service.task_service.get_user_tasks') as mock_get_tasks:
            
            mock_get_user.return_value = mock_user
            mock_get_tasks.return_value = []
            
            response = client.get("/api/tasks", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "tasks" in data
            assert "total" in data
    
    def test_get_tasks_unauthorized(self):
        """Test task retrieval without authentication."""
        response = client.get("/api/tasks")
        
        assert response.status_code == 401
    
    def test_create_task_success(self, mock_user, auth_headers):
        """Test successful task creation."""
        with patch('auth_service.get_current_user') as mock_get_user, \
             patch('task_service.task_service.create_task') as mock_create_task:
            
            mock_get_user.return_value = mock_user
            mock_create_task.return_value = {
                "task_id": "1",
                "userId": "A124242",
                "title": "Test Task",
                "details": "Test details",
                "due_date": "2025-12-31",
                "status": "To Do"
            }
            
            response = client.post(
                "/api/tasks",
                headers=auth_headers,
                json={
                    "title": "Test Task",
                    "details": "Test details",
                    "due_date": "2025-12-31",
                    "status": "To Do"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Test Task"
            assert data["userId"] == "A124242"
    
    def test_create_task_invalid_data(self, mock_user, auth_headers):
        """Test task creation with invalid data."""
        with patch('auth_service.get_current_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            response = client.post(
                "/api/tasks",
                headers=auth_headers,
                json={
                    "title": "",  # Invalid: empty title
                    "details": "Test details",
                    "due_date": "2025-12-31"
                }
            )
            
            assert response.status_code == 422  # Validation error
    
    def test_update_task_success(self, mock_user, auth_headers):
        """Test successful task update."""
        with patch('auth_service.get_current_user') as mock_get_user, \
             patch('task_service.task_service.update_task') as mock_update_task:
            
            mock_get_user.return_value = mock_user
            mock_update_task.return_value = {
                "task_id": "1",
                "userId": "A124242",
                "title": "Updated Task",
                "details": "Updated details",
                "due_date": "2025-12-31",
                "status": "In Progress"
            }
            
            response = client.put(
                "/api/tasks/1",
                headers=auth_headers,
                json={"status": "In Progress"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "In Progress"
    
    def test_update_task_not_found(self, mock_user, auth_headers):
        """Test updating non-existent task."""
        with patch('auth_service.get_current_user') as mock_get_user, \
             patch('task_service.task_service.update_task') as mock_update_task:
            
            mock_get_user.return_value = mock_user
            mock_update_task.side_effect = Exception("Task not found or access denied")
            
            response = client.put(
                "/api/tasks/999",
                headers=auth_headers,
                json={"status": "In Progress"}
            )
            
            assert response.status_code == 500
    
    def test_delete_task_success(self, mock_user, auth_headers):
        """Test successful task deletion."""
        with patch('auth_service.get_current_user') as mock_get_user, \
             patch('task_service.task_service.delete_task') as mock_delete_task:
            
            mock_get_user.return_value = mock_user
            mock_delete_task.return_value = True
            
            response = client.delete("/api/tasks/1", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Task deleted successfully"
            assert data["task_id"] == "1"
    
    def test_delete_task_not_found(self, mock_user, auth_headers):
        """Test deleting non-existent task."""
        with patch('auth_service.get_current_user') as mock_get_user, \
             patch('task_service.task_service.delete_task') as mock_delete_task:
            
            mock_get_user.return_value = mock_user
            mock_delete_task.side_effect = Exception("Task not found or access denied")
            
            response = client.delete("/api/tasks/999", headers=auth_headers)
            
            assert response.status_code == 500


class TestHealthEndpoints:
    """Test cases for health and info endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_api_info(self):
        """Test API info endpoint."""
        response = client.get("/api/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "version" in data
        assert "endpoints" in data


if __name__ == "__main__":
    pytest.main([__file__])
