/**
 * API service module
 * Following Single Responsibility Principle (SRP)
 * Provides centralized API communication with proper error handling
 */

import axios from 'axios'
import { API_CONFIG, STORAGE_CONFIG } from '../config'
import { storage, errorUtils } from '../utils'

// Create axios instance with configuration
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

/**
 * Request interceptor to add authentication token
 */
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = storage.getItem(STORAGE_CONFIG.KEYS.ACCESS_TOKEN)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Add request timestamp for debugging
    if (process.env.NODE_ENV === 'development') {
      config.metadata = { startTime: new Date() }
    }

    return config
  },
  (error) => {
    errorUtils.logError(error, 'Request Interceptor')
    return Promise.reject(error)
  }
)

/**
 * Response interceptor to handle common errors
 */
api.interceptors.response.use(
  (response) => {
    // Log response time in development
    if (process.env.NODE_ENV === 'development' && response.config.metadata) {
      const endTime = new Date()
      const duration = endTime - response.config.metadata.startTime
      console.log(`API Request: ${response.config.method?.toUpperCase()} ${response.config.url} - ${duration}ms`)
    }

    return response
  },
  (error) => {
    // Handle authentication errors
    if (error.response?.status === 401) {
      storage.clear()
      // Use router instead of window.location for better SPA behavior
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    // Log error
    errorUtils.logError(error, 'Response Interceptor')

    // Transform error for consistent handling
    const transformedError = {
      ...error,
      code: error.code || 'UNKNOWN_ERROR',
      message: errorUtils.getErrorMessage(error)
    }

    return Promise.reject(transformedError)
  }
)

/**
 * Generic API request method with retry logic
 * @param {Function} requestFn - Request function to execute
 * @param {number} retries - Number of retry attempts
 * @returns {Promise} - API response
 */
const apiRequest = async (requestFn, retries = API_CONFIG.RETRY_ATTEMPTS) => {
  try {
    return await requestFn()
  } catch (error) {
    if (retries > 0 && shouldRetry(error)) {
      console.log(`Retrying request... ${retries} attempts left`)
      await new Promise(resolve => setTimeout(resolve, 1000)) // Wait 1 second
      return apiRequest(requestFn, retries - 1)
    }
    throw error
  }
}

/**
 * Check if error should trigger a retry
 * @param {Error} error - Error object
 * @returns {boolean} - Should retry
 */
const shouldRetry = (error) => {
  // Retry on network errors or 5xx server errors
  return !error.response || (error.response.status >= 500 && error.response.status < 600)
}

/**
 * Authentication API service
 */
export const authAPI = {
  /**
   * Login user
   * @param {string} username - Username
   * @param {string} password - Password
   * @returns {Promise<object>} - Login response
   */
  login: async (username, password) => {
    return apiRequest(async () => {
      const response = await api.post(API_CONFIG.ENDPOINTS.AUTH.LOGIN, {
        username,
        password
      })
      return response.data
    })
  }
}

/**
 * Tasks API service
 */
export const tasksAPI = {
  /**
   * Get all tasks for the current user
   * @returns {Promise<object>} - Tasks response
   */
  getTasks: async () => {
    return apiRequest(async () => {
      const response = await api.get(API_CONFIG.ENDPOINTS.TASKS.GET_ALL)
      return response.data
    })
  },

  /**
   * Create a new task
   * @param {object} taskData - Task data
   * @returns {Promise<object>} - Created task
   */
  createTask: async (taskData) => {
    return apiRequest(async () => {
      const response = await api.post(API_CONFIG.ENDPOINTS.TASKS.CREATE, taskData)
      return response.data
    })
  },

  /**
   * Update an existing task
   * @param {string} taskId - Task ID
   * @param {object} updateData - Update data
   * @returns {Promise<object>} - Updated task
   */
  updateTask: async (taskId, updateData) => {
    return apiRequest(async () => {
      const response = await api.put(API_CONFIG.ENDPOINTS.TASKS.UPDATE(taskId), updateData)
      return response.data
    })
  },

  /**
   * Delete a task
   * @param {string} taskId - Task ID
   * @returns {Promise<object>} - Delete response
   */
  deleteTask: async (taskId) => {
    return apiRequest(async () => {
      const response = await api.delete(API_CONFIG.ENDPOINTS.TASKS.DELETE(taskId))
      return response.data
    })
  }
}

/**
 * Health check API service
 */
export const healthAPI = {
  /**
   * Check API health
   * @returns {Promise<object>} - Health response
   */
  check: async () => {
    return apiRequest(async () => {
      const response = await api.get('/')
      return response.data
    })
  },

  /**
   * Get API information
   * @returns {Promise<object>} - API info
   */
  info: async () => {
    return apiRequest(async () => {
      const response = await api.get('/api/info')
      return response.data
    })
  }
}

// Export the configured axios instance
export default api
