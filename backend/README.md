# Task Manager API - Refactored Backend

A modern, well-structured FastAPI backend for task management, following SOLID principles and Python best practices.

## 🏗️ Architecture Overview

The application follows a clean, modular architecture with clear separation of concerns:

```
backend/
├── app.py                 # Main FastAPI application
├── config.py             # Configuration and settings
├── models.py             # Pydantic data models
├── database_service.py   # Database abstraction layer
├── auth_service.py       # Authentication service
├── task_service.py       # Task business logic
├── routes.py             # API route definitions
├── test_api.py           # Comprehensive test suite
├── run_server.py         # Server runner script
└── requirements.txt      # Dependencies
```

## 🎯 SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- **`config.py`**: Only handles configuration and settings
- **`models.py`**: Only defines data models and validation
- **`database_service.py`**: Only handles database operations
- **`auth_service.py`**: Only handles authentication logic
- **`task_service.py`**: Only handles task business logic
- **`routes.py`**: Only defines API endpoints

### Open/Closed Principle (OCP)
- Database service uses abstract interface for extensibility
- Services can be extended without modifying existing code
- New authentication methods can be added without changing core logic

### Liskov Substitution Principle (LSP)
- Database implementations can be substituted without breaking functionality
- Service interfaces are properly defined and implemented

### Interface Segregation Principle (ISP)
- Database interface only includes necessary methods
- Services have focused, specific interfaces
- No client depends on methods it doesn't use

### Dependency Inversion Principle (DIP)
- High-level modules don't depend on low-level modules
- Both depend on abstractions (interfaces)
- Dependency injection used throughout

## 🚀 Key Features

### ✅ Code Quality Improvements
- **Type Hints**: Full type annotation coverage
- **Error Handling**: Comprehensive exception handling with custom exceptions
- **Logging**: Structured logging throughout the application
- **Validation**: Pydantic models with field validation
- **Documentation**: Comprehensive docstrings and API documentation

### ✅ Security Enhancements
- **Input Validation**: All inputs validated with Pydantic
- **Error Messages**: Sanitized error messages to prevent information leakage
- **Token Validation**: Proper JWT token validation
- **CORS Configuration**: Secure CORS setup

### ✅ Performance Optimizations
- **Dependency Injection**: Efficient dependency management
- **Database Abstraction**: Clean database operations
- **Async Support**: Full async/await support
- **Connection Pooling**: Ready for database connection pooling

### ✅ Maintainability
- **Modular Design**: Clear separation of concerns
- **Configuration Management**: Centralized configuration
- **Testing**: Comprehensive test coverage
- **Code Standards**: Following PEP 8 and Python best practices

## 📋 API Endpoints

### Authentication
- `POST /api/auth/login` - User authentication

### Tasks
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

### System
- `GET /` - Health check
- `GET /api/info` - API information
- `GET /docs` - Interactive API documentation (debug mode)

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- pip or poetry

### Installation

1. **Clone and navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run_server.py
   # OR
   python app.py
   ```

### Development Setup

1. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**:
   ```bash
   pytest test_api.py -v
   ```

3. **Code formatting**:
   ```bash
   black .
   isort .
   ```

4. **Linting**:
   ```bash
   flake8 .
   mypy .
   ```

## 🔧 Configuration

Configuration is managed through `config.py`:

```python
# API Configuration
API_TITLE = "Task Manager API"
API_VERSION = "1.0.0"
HOST = "10.0.0.8"
PORT = 8000

# Database Configuration
DATABASE_DIR = Path(__file__).parent.parent / "database"
USERS_FILE = DATABASE_DIR / "users.json"
TASKS_FILE = DATABASE_DIR / "tasks.json"

# Security Configuration
TOKEN_HEADER = "Authorization"
TOKEN_PREFIX = "Bearer "
```

## 🧪 Testing

The application includes comprehensive tests:

```bash
# Run all tests
pytest test_api.py -v

# Run with coverage
pytest test_api.py --cov=. --cov-report=html

# Run specific test class
pytest test_api.py::TestAuthentication -v
```

### Test Coverage
- ✅ Authentication endpoints
- ✅ Task CRUD operations
- ✅ Error handling
- ✅ Input validation
- ✅ Authorization
- ✅ Health checks

## 📊 Error Handling

The application implements comprehensive error handling:

### Custom Exceptions
- `DatabaseError`: Database operation failures
- `AuthenticationError`: Authentication failures
- `TaskError`: Task operation failures

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication failures)
- `404`: Not Found (resource not found)
- `500`: Internal Server Error (unexpected errors)

### Error Response Format
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE"
}
```

## 🔒 Security Features

### Input Validation
- All inputs validated with Pydantic models
- Field length limits and format validation
- SQL injection prevention (JSON-based storage)

### Authentication
- JWT token-based authentication
- Secure token validation
- User session management

### Error Handling
- Sanitized error messages
- No sensitive information leakage
- Proper HTTP status codes

## 📈 Performance Considerations

### Database Operations
- Efficient JSON file operations
- Minimal data loading
- Optimized queries

### Memory Management
- Proper resource cleanup
- Efficient data structures
- Connection pooling ready

### Caching Ready
- Service layer abstraction allows easy caching implementation
- Database operations can be cached
- Token validation can be cached

## 🚀 Deployment

### Production Deployment
1. Set `DEBUG=False` in configuration
2. Use production WSGI server (Gunicorn)
3. Configure proper logging
4. Set up monitoring

### Docker Support
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_server.py"]
```

## 📝 Code Standards

### PEP 8 Compliance
- Line length: 88 characters (Black formatter)
- Import organization (isort)
- Type hints throughout
- Comprehensive docstrings

### Documentation
- API documentation with FastAPI/OpenAPI
- Inline code documentation
- README files for each module
- Type hints for better IDE support

## 🔄 Future Enhancements

### Database Migration
- Easy migration to PostgreSQL/MySQL
- Database abstraction layer ready
- ORM integration possible

### Advanced Features
- Task categories and tags
- File attachments
- Real-time updates (WebSockets)
- Advanced search and filtering
- Task dependencies
- Time tracking

### Monitoring and Observability
- Health check endpoints
- Metrics collection
- Logging and monitoring
- Performance tracking

## 🤝 Contributing

1. Follow PEP 8 and Python best practices
2. Add comprehensive tests for new features
3. Update documentation
4. Use type hints
5. Follow SOLID principles

## 📄 License

This project is part of a coding challenge and is for educational purposes.
