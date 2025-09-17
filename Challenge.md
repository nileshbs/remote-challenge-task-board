Coding Challenge Requirements: Local Task Manager
This document outlines the requirements for a coding challenge to build a local task manager application. The challenge involves creating a full-stack application with a FastAPI backend and a Vue.js frontend, using a local JSON file as the database.

Core Components
Backend Framework: FastAPI

Frontend Framework: Vue.js

Database: Local JSON files stored in a folder named database.

Backend Functionality (FastAPI)
The backend will be responsible for handling all API requests, data persistence, and user authentication.

Data Structure:

Users: A users.json file will store user data, including a unique access_token (UUID) for each user.

Tasks: A separate JSON file (e.g., tasks.json) will store all tasks, with each task linked to a user via their userId.

Endpoints:

POST /login: Validates a user's credentials against users.json and returns the associated access_token. This endpoint should not require an access_token for authorization.

GET /tasks: Returns a list of tasks for the authenticated user. This endpoint must be protected and require a valid access_token in the request header.

POST /tasks: Adds a new task to the database for the authenticated user.

PUT /tasks/{task_id}: Updates an existing task's status or details. This is the primary endpoint for moving a task between columns.

DELETE /tasks/{task_id}: Removes a task from the database.

Frontend Functionality (Vue.js)
The frontend will provide the user interface for the task manager.

Authentication & Routing:

A login page will be the initial view. It should have fields for a username and password. Upon successful login, the user should be redirected to the main task board.

All subsequent pages and API calls will require the access_token to be stored and sent with each request. This token should persist to maintain the user's session.

Task Board:

A main dashboard will display the user's tasks organized into three distinct columns: To Do, In Progress, and Completed.

Each task will be represented by a card displaying its Title, Details, Due Date, and Status.

User Interactions:

Drag-and-Drop: Users must be able to drag a task card from one column to another. This action should trigger an API call to update the task's status on the backend.

Add Task: A button or form element will allow users to add a new task. This should open a modal or form with fields for Title, Details, and Due Date. The new task will be appended to the database with a default "To Do" status.

Delete Task: A trash can icon or a similar drag-and-drop target should be available. Dragging a task card onto the trash can will trigger an API call to remove the task from the database.

Search Functionality:

A search bar at the top of the page will filter the displayed tasks in real-time. The search should match text within both the Title and Details fields of the task cards. The search should not affect the columns, only which cards are visible.


Code Quality: The code should be clean, well-structured, and easy to read. Good practices for both FastAPI and Vue.js are expected.
