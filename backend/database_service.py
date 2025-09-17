"""
Database service layer for JSON file operations.

This module provides a clean abstraction for database operations,
following the Interface Segregation Principle (ISP) and Dependency Inversion Principle (DIP).
"""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import HTTPException

from config import settings

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


class DatabaseInterface(ABC):
    """Abstract interface for database operations."""
    
    @abstractmethod
    def load_data(self) -> List[Dict[str, Any]]:
        """Load data from the database."""
        pass
    
    @abstractmethod
    def save_data(self, data: List[Dict[str, Any]]) -> None:
        """Save data to the database."""
        pass
    
    @abstractmethod
    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Find an item by its ID."""
        pass
    
    @abstractmethod
    def find_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """Find items by a specific field value."""
        pass


class JSONDatabaseService(DatabaseInterface):
    """JSON file-based database service implementation."""
    
    def __init__(self, file_path: Path):
        """
        Initialize the JSON database service.
        
        Args:
            file_path: Path to the JSON database file
        """
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the database file exists."""
        if not self.file_path.exists():
            logger.warning(f"Database file {self.file_path} does not exist")
            raise DatabaseError(f"Database file not found: {self.file_path}")
    
    def load_data(self) -> List[Dict[str, Any]]:
        """
        Load data from the JSON file.
        
        Returns:
            List of dictionaries containing the data
            
        Raises:
            DatabaseError: If file cannot be read or parsed
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Loaded {len(data)} items from {self.file_path}")
                return data
        except FileNotFoundError:
            logger.error(f"Database file not found: {self.file_path}")
            raise DatabaseError(settings.ErrorMessages.DATABASE_NOT_FOUND)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in {self.file_path}: {e}")
            raise DatabaseError(settings.ErrorMessages.DATABASE_INVALID_FORMAT)
        except Exception as e:
            logger.error(f"Unexpected error loading data from {self.file_path}: {e}")
            raise DatabaseError(f"Failed to load data: {str(e)}")
    
    def save_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Save data to the JSON file.
        
        Args:
            data: List of dictionaries to save
            
        Raises:
            DatabaseError: If data cannot be saved
        """
        try:
            # Ensure directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                logger.info(f"Saved {len(data)} items to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save data to {self.file_path}: {e}")
            raise DatabaseError(f"{settings.ErrorMessages.SAVE_FAILED}: {str(e)}")
    
    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Find an item by its ID.
        
        Args:
            item_id: The ID to search for
            
        Returns:
            The item if found, None otherwise
        """
        data = self.load_data()
        for item in data:
            if item.get('task_id') == item_id or item.get('userId') == item_id:
                return item
        return None
    
    def find_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """
        Find items by a specific field value.
        
        Args:
            field: The field name to search
            value: The value to match
            
        Returns:
            List of matching items
        """
        data = self.load_data()
        return [item for item in data if item.get(field) == value]
    
    def add_item(self, item: Dict[str, Any]) -> None:
        """
        Add a new item to the database.
        
        Args:
            item: The item to add
        """
        data = self.load_data()
        data.append(item)
        self.save_data(data)
    
    def update_item(self, item_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update an existing item in the database.
        
        Args:
            item_id: The ID of the item to update
            update_data: Dictionary of fields to update
            
        Returns:
            True if item was updated, False if not found
        """
        data = self.load_data()
        for i, item in enumerate(data):
            if item.get('task_id') == item_id:
                # Update only provided fields
                for key, value in update_data.items():
                    if value is not None:
                        data[i][key] = value
                self.save_data(data)
                return True
        return False
    
    def remove_item(self, item_id: str) -> bool:
        """
        Remove an item from the database.
        
        Args:
            item_id: The ID of the item to remove
            
        Returns:
            True if item was removed, False if not found
        """
        data = self.load_data()
        for i, item in enumerate(data):
            if item.get('task_id') == item_id:
                removed_item = data.pop(i)
                self.save_data(data)
                logger.info(f"Removed item {item_id} from database")
                return True
        return False
    
    def get_next_id(self, id_field: str = 'task_id') -> str:
        """
        Generate the next available ID.
        
        Args:
            id_field: The field name that contains the ID
            
        Returns:
            The next available ID as a string
        """
        data = self.load_data()
        if not data:
            return "1"
        
        max_id = 0
        for item in data:
            try:
                item_id = int(item.get(id_field, '0'))
                max_id = max(max_id, item_id)
            except (ValueError, TypeError):
                continue
        
        return str(max_id + 1)


class DatabaseServiceFactory:
    """Factory class for creating database services."""
    
    @staticmethod
    def create_users_service() -> JSONDatabaseService:
        """Create a users database service."""
        return JSONDatabaseService(settings.USERS_FILE)
    
    @staticmethod
    def create_tasks_service() -> JSONDatabaseService:
        """Create a tasks database service."""
        return JSONDatabaseService(settings.TASKS_FILE)
