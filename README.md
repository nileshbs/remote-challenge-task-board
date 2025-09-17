# Hello World Project - FastAPI + Vue.js

A simple hello world application with a FastAPI backend and Vue.js frontend.

## Project Structure

```
remote-challenge/
├── backend/          # FastAPI backend
│   ├── main.py       # Main application file
│   ├── run_local.py  # Local development server
│   └── requirements.txt
├── frontend/         # Vue.js frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python run_local.py
   ```

The backend will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at: http://localhost:3000

## Testing the Connection

1. Start both the backend and frontend servers (see instructions above)
2. Open the frontend in your browser (http://localhost:3000)
3. Click the "Test Backend Connection" button to verify communication between frontend and backend

## Features

- **Backend**: FastAPI with CORS enabled for frontend communication
- **Frontend**: Vue.js 3 with Vite for fast development
- **API Testing**: Interactive button to test backend connectivity
- **Hot Reload**: Both frontend and backend support hot reload during development

## API Endpoints

- `GET /` - Root endpoint with hello message
- `GET /api/hello` - API endpoint that returns a JSON response
