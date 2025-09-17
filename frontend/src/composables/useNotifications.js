/**
 * Notifications composable
 * Following Single Responsibility Principle (SRP)
 * Provides notification system for user feedback
 */

import { ref, reactive } from 'vue'
import { SUCCESS_MESSAGES, ERROR_MESSAGES } from '../config'

// Global notification state
const notifications = ref([])
let notificationId = 0

/**
 * Notification types
 */
export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
}

/**
 * Default notification configuration
 */
const DEFAULT_CONFIG = {
  duration: 5000, // 5 seconds
  position: 'top-right',
  closable: true,
  persistent: false
}

/**
 * Notifications composable
 * @returns {object} Notification state and methods
 */
export function useNotifications() {
  /**
   * Add a new notification
   * @param {string} message - Notification message
   * @param {string} type - Notification type
   * @param {object} config - Notification configuration
   * @returns {number} - Notification ID
   */
  const addNotification = (message, type = NOTIFICATION_TYPES.INFO, config = {}) => {
    const id = ++notificationId
    const notification = {
      id,
      message,
      type,
      timestamp: Date.now(),
      ...DEFAULT_CONFIG,
      ...config
    }

    notifications.value.push(notification)

    // Auto-remove notification if not persistent
    if (!notification.persistent && notification.duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, notification.duration)
    }

    return id
  }

  /**
   * Remove a notification
   * @param {number} id - Notification ID
   */
  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  /**
   * Clear all notifications
   */
  const clearAllNotifications = () => {
    notifications.value = []
  }

  /**
   * Show success notification
   * @param {string} message - Success message
   * @param {object} config - Configuration
   * @returns {number} - Notification ID
   */
  const showSuccess = (message, config = {}) => {
    return addNotification(message, NOTIFICATION_TYPES.SUCCESS, config)
  }

  /**
   * Show error notification
   * @param {string} message - Error message
   * @param {object} config - Configuration
   * @returns {number} - Notification ID
   */
  const showError = (message, config = {}) => {
    return addNotification(message, NOTIFICATION_TYPES.ERROR, {
      persistent: true, // Errors should be persistent by default
      ...config
    })
  }

  /**
   * Show warning notification
   * @param {string} message - Warning message
   * @param {object} config - Configuration
   * @returns {number} - Notification ID
   */
  const showWarning = (message, config = {}) => {
    return addNotification(message, NOTIFICATION_TYPES.WARNING, config)
  }

  /**
   * Show info notification
   * @param {string} message - Info message
   * @param {object} config - Configuration
   * @returns {number} - Notification ID
   */
  const showInfo = (message, config = {}) => {
    return addNotification(message, NOTIFICATION_TYPES.INFO, config)
  }

  /**
   * Show task-related success notifications
   */
  const taskNotifications = {
    created: () => showSuccess(SUCCESS_MESSAGES.TASK_CREATED),
    updated: () => showSuccess(SUCCESS_MESSAGES.TASK_UPDATED),
    deleted: () => showSuccess(SUCCESS_MESSAGES.TASK_DELETED),
    moved: () => showSuccess(SUCCESS_MESSAGES.TASK_MOVED)
  }

  /**
   * Show auth-related notifications
   */
  const authNotifications = {
    loginSuccess: () => showSuccess(SUCCESS_MESSAGES.LOGIN),
    logoutSuccess: () => showSuccess(SUCCESS_MESSAGES.LOGOUT),
    loginError: (error) => showError(error || ERROR_MESSAGES.UNAUTHORIZED)
  }

  return {
    // State
    notifications: notifications.value,
    
    // Methods
    addNotification,
    removeNotification,
    clearAllNotifications,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    taskNotifications,
    authNotifications
  }
}

// Export global state for use in components
export { notifications }
