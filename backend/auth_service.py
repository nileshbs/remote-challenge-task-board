"""
Authentication service for user management and token validation.

This module handles all authentication-related operations, following the
Single Responsibility Principle (SRP) and providing a clean interface.
"""

import logging
from typing import Optional
from fastapi import HTTPException, Depends, Header

from models import UserInfo
from database_service import DatabaseServiceFactory, DatabaseError
from config import settings

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class AuthenticationService:
    """Service class for handling authentication operations."""
    
    def __init__(self):
        """Initialize the authentication service."""
        self.users_db = DatabaseServiceFactory.create_users_service()
    
    def authenticate_user(self, username: str, password: str) -> Optional[UserInfo]:
        """
        Authenticate user credentials.
        
        Args:
            username: The username to authenticate
            password: The password to verify
            
        Returns:
            UserInfo object if authentication successful, None otherwise
            
        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            users = self.users_db.find_by_field('username', username)
            
            for user in users:
                if user.get('password') == password:
                    return UserInfo(
                        user_id=user.get('userId'),
                        username=user.get('username'),
                        first_name=user.get('firstName'),
                        last_name=user.get('lastName'),
                        access_token=user.get('access_token')
                    )
            
            logger.warning(f"Failed authentication attempt for username: {username}")
            return None
            
        except DatabaseError as e:
            logger.error(f"Database error during authentication: {e}")
            raise AuthenticationError("Authentication service unavailable")
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            raise AuthenticationError("Authentication failed")
    
    def get_user_by_token(self, access_token: str) -> Optional[UserInfo]:
        """
        Get user information by access token.
        
        Args:
            access_token: The access token to validate
            
        Returns:
            UserInfo object if token is valid, None otherwise
            
        Raises:
            AuthenticationError: If token validation fails
        """
        try:
            users = self.users_db.find_by_field('access_token', access_token)
            
            if users:
                user = users[0]  # Should be unique
                return UserInfo(
                    user_id=user.get('userId'),
                    username=user.get('username'),
                    first_name=user.get('firstName'),
                    last_name=user.get('lastName'),
                    access_token=user.get('access_token')
                )
            
            logger.warning(f"Invalid token access attempt: {access_token[:10]}...")
            return None
            
        except DatabaseError as e:
            logger.error(f"Database error during token validation: {e}")
            raise AuthenticationError("Authentication service unavailable")
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {e}")
            raise AuthenticationError("Token validation failed")
    
    def validate_token_format(self, authorization_header: str) -> str:
        """
        Validate and extract token from authorization header.
        
        Args:
            authorization_header: The Authorization header value
            
        Returns:
            The extracted token
            
        Raises:
            HTTPException: If token format is invalid
        """
        if not authorization_header:
            raise HTTPException(
                status_code=401,
                detail=settings.ErrorMessages.TOKEN_MISSING
            )
        
        if not authorization_header.startswith(settings.TOKEN_PREFIX):
            raise HTTPException(
                status_code=401,
                detail=settings.ErrorMessages.TOKEN_INVALID_FORMAT
            )
        
        token = authorization_header[len(settings.TOKEN_PREFIX):].strip()
        if not token:
            raise HTTPException(
                status_code=401,
                detail=settings.ErrorMessages.TOKEN_INVALID_FORMAT
            )
        
        return token


# Global authentication service instance
auth_service = AuthenticationService()


def get_current_user(authorization: str = Header(None)) -> UserInfo:
    """
    FastAPI dependency to get the current authenticated user.
    
    Args:
        authorization: The Authorization header
        
    Returns:
        UserInfo object for the authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Extract and validate token
        token = auth_service.validate_token_format(authorization)
        
        # Get user by token
        user = auth_service.get_user_by_token(token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail=settings.ErrorMessages.TOKEN_INVALID
            )
        
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Authentication service error"
        )
    except Exception as e:
        logger.error(f"Unexpected authentication error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
