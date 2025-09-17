from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from datetime import datetime

app = FastAPI(title="Hello World API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.0.0.8:3000", "http://10.0.0.8:5173", "http://10.0.0.8:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    user_id: str
    username: str
    first_name: str
    last_name: str

class TaskRequest(BaseModel):
    title: str
    details: str
    due_date: str
    status: str = "To Do"

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    details: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    userId: str
    title: str
    details: str
    due_date: str
    status: str

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

# Authentication service
def load_users():
    """Load users from users.json file"""
    try:
        # Get the path to users.json relative to the backend directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        users_file = os.path.join(current_dir, '..', 'database', 'users.json')
        
        with open(users_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Users database not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid users database format")

def authenticate_user(username: str, password: str):
    """Authenticate user credentials against users.json"""
    users = load_users()
    
    for user in users:
        if user.get('username') == username and user.get('password') == password:
            return {
                'access_token': user.get('access_token'),
                'user_id': user.get('userId'),
                'username': user.get('username'),
                'first_name': user.get('firstName'),
                'last_name': user.get('lastName')
            }
    
    return None

def get_user_by_token(access_token: str):
    """Get user information by access token"""
    users = load_users()
    
    for user in users:
        if user.get('access_token') == access_token:
            return {
                'user_id': user.get('userId'),
                'username': user.get('username'),
                'first_name': user.get('firstName'),
                'last_name': user.get('lastName')
            }
    
    return None

def verify_token(authorization: str = Header(None)):
    """Verify access token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.split(" ")[1]
    user = get_user_by_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user

# Task service functions
def load_tasks():
    """Load tasks from tasks.json file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tasks_file = os.path.join(current_dir, '..', 'database', 'tasks.json')
        
        with open(tasks_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Tasks database not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid tasks database format")

def save_tasks(tasks):
    """Save tasks to tasks.json file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tasks_file = os.path.join(current_dir, '..', 'database', 'tasks.json')
        
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save tasks: {str(e)}")

def get_next_task_id():
    """Generate next available task ID"""
    tasks = load_tasks()
    if not tasks:
        return "1"
    
    max_id = 0
    for task in tasks:
        try:
            task_id = int(task.get('task_id', '0'))
            max_id = max(max_id, task_id)
        except ValueError:
            continue
    
    return str(max_id + 1)

def get_task_by_id(task_id: str, user_id: str):
    """Get a specific task by ID, ensuring it belongs to the user"""
    tasks = load_tasks()
    
    for task in tasks:
        if task.get('task_id') == task_id and task.get('userId') == user_id:
            return task
    
    return None

def update_task_in_list(tasks: list, task_id: str, user_id: str, update_data: dict):
    """Update a task in the tasks list"""
    for i, task in enumerate(tasks):
        if task.get('task_id') == task_id and task.get('userId') == user_id:
            # Update only provided fields
            for key, value in update_data.items():
                if value is not None:
                    task[key] = value
            return True
    return False

def remove_task_from_list(tasks: list, task_id: str, user_id: str):
    """Remove a task from the tasks list"""
    for i, task in enumerate(tasks):
        if task.get('task_id') == task_id and task.get('userId') == user_id:
            return tasks.pop(i)
    return None

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI!"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from the backend!", "status": "success"}

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """
    Authenticate user credentials and return access token
    """
    user_data = authenticate_user(login_request.username, login_request.password)
    
    if user_data is None:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password"
        )
    
    return LoginResponse(
        access_token=user_data['access_token'],
        user_id=user_data['user_id'],
        username=user_data['username'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )

@app.get("/api/tasks", response_model=TaskListResponse)
async def get_user_tasks(current_user: dict = Depends(verify_token)):
    """
    Get all tasks for the authenticated user
    """
    tasks = load_tasks()
    user_tasks = [
        TaskResponse(
            task_id=task.get('task_id'),
            userId=task.get('userId'),
            title=task.get('title'),
            details=task.get('details'),
            due_date=task.get('due_date'),
            status=task.get('status')
        )
        for task in tasks[:len(tasks)-5]  # Limit to first 100 tasks
        if task.get('userId') == current_user['user_id']
    ]
    
    return TaskListResponse(tasks=user_tasks)

@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(
    task_request: TaskRequest,
    current_user: dict = Depends(verify_token)
):
    """
    Create a new task for the authenticated user
    """
    tasks = load_tasks()
    
    # Generate new task ID
    new_task_id = get_next_task_id()
    
    # Create new task
    new_task = {
        "task_id": new_task_id,
        "userId": current_user['user_id'],
        "title": task_request.title,
        "details": task_request.details,
        "due_date": task_request.due_date,
        "status": task_request.status
    }
    
    # Add to tasks list and save
    tasks.append(new_task)
    save_tasks(tasks)
    
    return TaskResponse(
        task_id=new_task['task_id'],
        userId=new_task['userId'],
        title=new_task['title'],
        details=new_task['details'],
        due_date=new_task['due_date'],
        status=new_task['status']
    )

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdateRequest,
    current_user: dict = Depends(verify_token)
):
    """
    Update a task for the authenticated user
    """
    # Check if task exists and belongs to user
    existing_task = get_task_by_id(task_id, current_user['user_id'])
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    
    # Load all tasks
    tasks = load_tasks()
    
    # Prepare update data (only include non-None values)
    update_data = {}
    if task_update.title is not None:
        update_data['title'] = task_update.title
    if task_update.details is not None:
        update_data['details'] = task_update.details
    if task_update.due_date is not None:
        update_data['due_date'] = task_update.due_date
    if task_update.status is not None:
        update_data['status'] = task_update.status
    
    # Check if there's anything to update
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    # Update the task
    success = update_task_in_list(tasks, task_id, current_user['user_id'], update_data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    # Save updated tasks
    save_tasks(tasks)
    
    # Get the updated task
    updated_task = get_task_by_id(task_id, current_user['user_id'])
    
    return TaskResponse(
        task_id=updated_task['task_id'],
        userId=updated_task['userId'],
        title=updated_task['title'],
        details=updated_task['details'],
        due_date=updated_task['due_date'],
        status=updated_task['status']
    )

@app.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(verify_token)
):
    """
    Delete a task for the authenticated user
    """
    # Check if task exists and belongs to user
    existing_task = get_task_by_id(task_id, current_user['user_id'])
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    
    # Load all tasks
    tasks = load_tasks()
    
    # Remove the task
    removed_task = remove_task_from_list(tasks, task_id, current_user['user_id'])
    if not removed_task:
        raise HTTPException(status_code=500, detail="Failed to delete task")
    
    # Save updated tasks
    save_tasks(tasks)
    
    return {"message": "Task deleted successfully", "task_id": task_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.0.0.8", port=8000)
