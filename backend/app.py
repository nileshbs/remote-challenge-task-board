"""
Main FastAPI application module.

This module creates and configures the FastAPI application with proper
middleware, error handling, and route registration.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from routes import auth_router, tasks_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    
    Args:
        app: The FastAPI application instance
    """
    # Startup
    logger.info("Starting Task Manager API...")
    logger.info(f"API Title: {settings.API_TITLE}")
    logger.info(f"API Version: {settings.API_VERSION}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    
    # Verify database files exist
    try:
        if not settings.USERS_FILE.exists():
            logger.warning(f"Users database file not found: {settings.USERS_FILE}")
        if not settings.TASKS_FILE.exists():
            logger.warning(f"Tasks database file not found: {settings.TASKS_FILE}")
    except Exception as e:
        logger.error(f"Error checking database files: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Task Manager API...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests."""
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions globally."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # Include routers
    app.include_router(auth_router)
    app.include_router(tasks_router)
    
    # Health check endpoint
    @app.get("/", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "message": "Task Manager API is running",
            "version": settings.API_VERSION,
            "status": "healthy"
        }
    
    # API info endpoint
    @app.get("/api/info", tags=["Info"])
    async def api_info():
        """API information endpoint."""
        return {
            "title": settings.API_TITLE,
            "version": settings.API_VERSION,
            "description": settings.API_DESCRIPTION,
            "endpoints": {
                "authentication": "/api/auth",
                "tasks": "/api/tasks",
                "documentation": "/docs" if settings.DEBUG else "disabled"
            }
        }
    
    return app


# Create the application instance
app = create_app()


def main():
    """Main function to run the application."""
    logger.info("Starting Task Manager API server...")
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )


if __name__ == "__main__":
    main()
