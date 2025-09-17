/**
 * Application configuration and constants
 * Following Single Responsibility Principle (SRP)
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://10.0.0.8:8000',
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/api/auth/login'
    },
    TASKS: {
      BASE: '/api/tasks',
      GET_ALL: '/api/tasks',
      CREATE: '/api/tasks',
      UPDATE: (id) => `/api/tasks/${id}`,
      DELETE: (id) => `/api/tasks/${id}`
    }
  },
  TIMEOUT: 10000, // 10 seconds
  RETRY_ATTEMPTS: 3
}

// Application Configuration
export const APP_CONFIG = {
  NAME: 'Task Manager',
  VERSION: '1.0.0',
  DESCRIPTION: 'A modern task management application',
  ROUTES: {
    LOGIN: '/login',
    TASKBOARD: '/taskboard',
    HOME: '/'
  }
}

// Task Configuration
export const TASK_CONFIG = {
  STATUSES: {
    TODO: 'To Do',
    IN_PROGRESS: 'In Progress',
    COMPLETED: 'Completed'
  },
  VALID_STATUSES: ['To Do', 'In Progress', 'Completed'],
  DEFAULT_STATUS: 'To Do',
  VALIDATION: {
    TITLE_MAX_LENGTH: 200,
    DETAILS_MAX_LENGTH: 1000,
    DUE_DATE_FORMAT: 'YYYY-MM-DD'
  }
}

// UI Configuration
export const UI_CONFIG = {
  ANIMATION: {
    DURATION: 300,
    EASING: 'ease-in-out'
  },
  BREAKPOINTS: {
    MOBILE: 768,
    TABLET: 1024,
    DESKTOP: 1200
  },
  COLORS: {
    PRIMARY: '#667eea',
    SECONDARY: '#764ba2',
    SUCCESS: '#28a745',
    WARNING: '#fd7e14',
    DANGER: '#dc3545',
    INFO: '#17a2b8',
    LIGHT: '#f8f9fa',
    DARK: '#343a40'
  },
  SPACING: {
    XS: '0.25rem',
    SM: '0.5rem',
    MD: '1rem',
    LG: '1.5rem',
    XL: '2rem',
    XXL: '3rem'
  }
}

// Storage Configuration
export const STORAGE_CONFIG = {
  KEYS: {
    ACCESS_TOKEN: 'access_token',
    USER_DATA: 'user_data',
    THEME: 'theme',
    SETTINGS: 'settings'
  },
  EXPIRY: {
    TOKEN: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
    USER_DATA: 24 * 60 * 60 * 1000 // 24 hours in milliseconds
  }
}

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized. Please login again.',
  FORBIDDEN: 'Access denied.',
  NOT_FOUND: 'Resource not found.',
  VALIDATION: 'Please check your input and try again.',
  SERVER: 'Server error. Please try again later.',
  TIMEOUT: 'Request timeout. Please try again.',
  UNKNOWN: 'An unexpected error occurred.'
}

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN: 'Login successful!',
  LOGOUT: 'Logged out successfully!',
  TASK_CREATED: 'Task created successfully!',
  TASK_UPDATED: 'Task updated successfully!',
  TASK_DELETED: 'Task deleted successfully!',
  TASK_MOVED: 'Task moved successfully!'
}

// Development Configuration
export const DEV_CONFIG = {
  DEBUG: process.env.NODE_ENV === 'development',
  LOG_LEVEL: process.env.NODE_ENV === 'development' ? 'debug' : 'error',
  MOCK_API: false,
  ENABLE_DEVTOOLS: process.env.NODE_ENV === 'development'
}

// Export all configurations as a single object
export const CONFIG = {
  API: API_CONFIG,
  APP: APP_CONFIG,
  TASK: TASK_CONFIG,
  UI: UI_CONFIG,
  STORAGE: STORAGE_CONFIG,
  ERRORS: ERROR_MESSAGES,
  SUCCESS: SUCCESS_MESSAGES,
  DEV: DEV_CONFIG
}

export default CONFIG
