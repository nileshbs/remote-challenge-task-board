# Task Manager - Complete Setup Guide

This guide will help you set up and run the complete Task Manager application with Vue.js frontend and FastAPI backend.

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- npm or yarn

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the backend server:
   ```bash
   ~~python main.py~~
   python .\run_server.py
```

The backend will be available at `http://10.0.0.8:8000`

## Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Use the demo credentials to login:
   - **Username**: johndoe
   - **Password**: password123
3. Start managing your tasks!

## Features

### ✅ Implemented Features

- **Authentication**: Login with username/password
- **Task Board**: Three-column Kanban board (To Do, In Progress, Completed)
- **Drag & Drop**: Drag tasks between columns to update status
- **Add Tasks**: Create new tasks with title, details, and due date
- **Edit Tasks**: Update existing task details
- **Delete Tasks**: Remove tasks by dragging to trash or clicking delete button
- **Responsive Design**: Works on desktop and mobile devices

### 🔧 Technical Implementation

- **Backend**: FastAPI with JWT authentication
- **Frontend**: Vue.js 3 with Composition API
- **Database**: JSON files (users.json, tasks.json)
- **Drag & Drop**: Native HTML5 drag and drop API
- **State Management**: Vue 3 reactive system with localStorage

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login

### Tasks
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

## Demo Data

The application comes with pre-populated demo data:
- 5 users with different credentials
- Multiple tasks across different statuses
- Various due dates and details

## Troubleshooting

### Backend Issues
- Ensure Python virtual environment is activated
- Check that all dependencies are installed
- Verify the server is running on the correct port

### Frontend Issues
- Clear browser cache and localStorage
- Check browser console for errors
- Ensure backend is running before starting frontend

### CORS Issues
- The backend is configured to allow requests from common development ports
- If you encounter CORS errors, check the backend CORS configuration in `main.py`

## Development

### Backend Development
- The backend uses FastAPI with automatic API documentation
- Visit `http://10.0.0.8:8000/docs` for interactive API documentation
- All endpoints include proper error handling and validation

### Frontend Development
- Uses Vue 3 Composition API for modern development
- Hot reload enabled for development
- Responsive design with CSS Grid and Flexbox

## Production Deployment

### Backend
1. Set up a production WSGI server (e.g., Gunicorn)
2. Configure environment variables
3. Set up proper database (replace JSON files)

### Frontend
1. Build the production bundle: `npm run build`
2. Serve the `dist` folder with a web server
3. Configure API URL for production backend

## Support

For issues or questions:
1. Check the console for error messages
2. Verify all setup steps are completed
3. Ensure both backend and frontend are running
4. Check network connectivity between frontend and backend
