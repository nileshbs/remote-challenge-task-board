/**
 * Utility functions for the application
 * Following Single Responsibility Principle (SRP)
 */

import { STORAGE_CONFIG, ERROR_MESSAGES } from '../config'

/**
 * Storage utilities for localStorage operations
 */
export const storage = {
  /**
   * Set item in localStorage with optional expiry
   * @param {string} key - Storage key
   * @param {any} value - Value to store
   * @param {number} expiry - Expiry time in milliseconds
   */
  setItem(key, value, expiry = null) {
    try {
      const item = {
        value,
        timestamp: Date.now(),
        expiry: expiry ? Date.now() + expiry : null
      }
      localStorage.setItem(key, JSON.stringify(item))
    } catch (error) {
      console.error('Error setting localStorage item:', error)
    }
  },

  /**
   * Get item from localStorage with expiry check
   * @param {string} key - Storage key
   * @returns {any|null} - Stored value or null
   */
  getItem(key) {
    try {
      const item = localStorage.getItem(key)
      if (!item) return null

      const parsed = JSON.parse(item)
      
      // Check if item has expired
      if (parsed.expiry && Date.now() > parsed.expiry) {
        this.removeItem(key)
        return null
      }

      return parsed.value
    } catch (error) {
      console.error('Error getting localStorage item:', error)
      return null
    }
  },

  /**
   * Remove item from localStorage
   * @param {string} key - Storage key
   */
  removeItem(key) {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Error removing localStorage item:', error)
    }
  },

  /**
   * Clear all application data from localStorage
   */
  clear() {
    try {
      Object.values(STORAGE_CONFIG.KEYS).forEach(key => {
        localStorage.removeItem(key)
      })
    } catch (error) {
      console.error('Error clearing localStorage:', error)
    }
  }
}

/**
 * Date utilities
 */
export const dateUtils = {
  /**
   * Format date to YYYY-MM-DD format
   * @param {Date|string} date - Date to format
   * @returns {string} - Formatted date string
   */
  formatDate(date) {
    try {
      const d = new Date(date)
      return d.toISOString().split('T')[0]
    } catch (error) {
      console.error('Error formatting date:', error)
      return ''
    }
  },

  /**
   * Format date for display
   * @param {Date|string} date - Date to format
   * @returns {string} - Formatted date string
   */
  formatDisplayDate(date) {
    try {
      const d = new Date(date)
      return d.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      })
    } catch (error) {
      console.error('Error formatting display date:', error)
      return date
    }
  },

  /**
   * Get date class for styling based on due date
   * @param {Date|string} dueDate - Due date
   * @returns {string} - CSS class name
   */
  getDateClass(dueDate) {
    try {
      const date = new Date(dueDate)
      const today = new Date()
      const diffTime = date - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) return 'overdue'
      if (diffDays <= 3) return 'due-soon'
      return 'due-normal'
    } catch (error) {
      console.error('Error getting date class:', error)
      return 'due-normal'
    }
  },

  /**
   * Get tomorrow's date in YYYY-MM-DD format
   * @returns {string} - Tomorrow's date
   */
  getTomorrow() {
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    return this.formatDate(tomorrow)
  }
}

/**
 * Validation utilities
 */
export const validation = {
  /**
   * Validate email format
   * @param {string} email - Email to validate
   * @returns {boolean} - Is valid email
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  },

  /**
   * Validate required field
   * @param {any} value - Value to validate
   * @returns {boolean} - Is valid
   */
  isRequired(value) {
    return value !== null && value !== undefined && value !== ''
  },

  /**
   * Validate string length
   * @param {string} value - String to validate
   * @param {number} min - Minimum length
   * @param {number} max - Maximum length
   * @returns {boolean} - Is valid length
   */
  isValidLength(value, min = 0, max = Infinity) {
    if (typeof value !== 'string') return false
    return value.length >= min && value.length <= max
  },

  /**
   * Validate task data
   * @param {object} taskData - Task data to validate
   * @returns {object} - Validation result
   */
  validateTask(taskData) {
    const errors = []

    if (!this.isRequired(taskData.title)) {
      errors.push('Title is required')
    } else if (!this.isValidLength(taskData.title, 1, 200)) {
      errors.push('Title must be between 1 and 200 characters')
    }

    if (taskData.details && !this.isValidLength(taskData.details, 0, 1000)) {
      errors.push('Details must be less than 1000 characters')
    }

    if (!this.isRequired(taskData.due_date)) {
      errors.push('Due date is required')
    }

    return {
      isValid: errors.length === 0,
      errors
    }
  }
}

/**
 * Error handling utilities
 */
export const errorUtils = {
  /**
   * Get user-friendly error message
   * @param {Error|object} error - Error object
   * @returns {string} - User-friendly error message
   */
  getErrorMessage(error) {
    if (!error) return ERROR_MESSAGES.UNKNOWN

    // Network errors
    if (error.code === 'NETWORK_ERROR' || !error.response) {
      return ERROR_MESSAGES.NETWORK
    }

    // HTTP status errors
    const status = error.response?.status
    switch (status) {
      case 401:
        return ERROR_MESSAGES.UNAUTHORIZED
      case 403:
        return ERROR_MESSAGES.FORBIDDEN
      case 404:
        return ERROR_MESSAGES.NOT_FOUND
      case 422:
        return ERROR_MESSAGES.VALIDATION
      case 500:
        return ERROR_MESSAGES.SERVER
      default:
        return error.response?.data?.detail || ERROR_MESSAGES.UNKNOWN
    }
  },

  /**
   * Log error with context
   * @param {Error|object} error - Error object
   * @param {string} context - Error context
   */
  logError(error, context = '') {
    console.error(`[${context}] Error:`, error)
    
    // In production, you might want to send errors to a logging service
    if (process.env.NODE_ENV === 'production') {
      // Example: send to error tracking service
      // errorTrackingService.captureException(error, { context })
    }
  }
}

/**
 * DOM utilities
 */
export const domUtils = {
  /**
   * Smooth scroll to element
   * @param {string|HTMLElement} element - Element selector or element
   * @param {object} options - Scroll options
   */
  scrollTo(element, options = {}) {
    try {
      const el = typeof element === 'string' ? document.querySelector(element) : element
      if (el) {
        el.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
          ...options
        })
      }
    } catch (error) {
      console.error('Error scrolling to element:', error)
    }
  },

  /**
   * Focus element
   * @param {string|HTMLElement} element - Element selector or element
   */
  focus(element) {
    try {
      const el = typeof element === 'string' ? document.querySelector(element) : element
      if (el) {
        el.focus()
      }
    } catch (error) {
      console.error('Error focusing element:', error)
    }
  }
}

/**
 * Array utilities
 */
export const arrayUtils = {
  /**
   * Group array by key
   * @param {Array} array - Array to group
   * @param {string} key - Key to group by
   * @returns {object} - Grouped object
   */
  groupBy(array, key) {
    return array.reduce((groups, item) => {
      const group = item[key]
      groups[group] = groups[group] || []
      groups[group].push(item)
      return groups
    }, {})
  },

  /**
   * Remove duplicates from array
   * @param {Array} array - Array to deduplicate
   * @param {string} key - Key to check for duplicates
   * @returns {Array} - Deduplicated array
   */
  uniqueBy(array, key) {
    const seen = new Set()
    return array.filter(item => {
      const value = item[key]
      if (seen.has(value)) {
        return false
      }
      seen.add(value)
      return true
    })
  }
}

/**
 * Debounce utility
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * Throttle utility
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} - Throttled function
 */
export const throttle = (func, limit) => {
  let inThrottle
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * Search utilities
 */
export const searchUtils = {
  /**
   * Filter tasks based on search query
   * @param {Array} tasks - Array of tasks to filter
   * @param {string} query - Search query
   * @param {Array} fields - Fields to search in (default: ['title', 'details'])
   * @returns {Array} - Filtered tasks
   */
  filterTasks: (tasks, query, fields = ['title', 'details']) => {
    if (!query || !query.trim()) {
      return tasks
    }
    
    const searchQuery = query.toLowerCase().trim()
    return tasks.filter(task => {
      return fields.some(field => {
        const value = (task[field] || '').toLowerCase()
        return value.includes(searchQuery)
      })
    })
  },

  /**
   * Highlight search terms in text
   * @param {string} text - Text to highlight
   * @param {string} query - Search query
   * @returns {string} - HTML with highlighted terms
   */
  highlightSearchTerms: (text, query) => {
    if (!query || !query.trim()) {
      return text
    }
    
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
    return text.replace(regex, '<mark>$1</mark>')
  },

  /**
   * Get search suggestions based on task data
   * @param {Array} tasks - Array of tasks
   * @param {string} query - Partial search query
   * @param {number} limit - Maximum number of suggestions
   * @returns {Array} - Array of suggestion strings
   */
  getSearchSuggestions: (tasks, query, limit = 5) => {
    if (!query || query.length < 2) {
      return []
    }
    
    const suggestions = new Set()
    const searchQuery = query.toLowerCase()
    
    tasks.forEach(task => {
      // Add title suggestions
      if (task.title && task.title.toLowerCase().includes(searchQuery)) {
        suggestions.add(task.title)
      }
      
      // Add details suggestions (extract words)
      if (task.details) {
        const words = task.details.toLowerCase().split(/\s+/)
        words.forEach(word => {
          if (word.includes(searchQuery) && word.length > 2) {
            suggestions.add(word)
          }
        })
      }
    })
    
    return Array.from(suggestions).slice(0, limit)
  }
}
