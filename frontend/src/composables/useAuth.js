/**
 * Authentication composable
 * Following Single Responsibility Principle (SRP)
 * Provides authentication state and methods
 */

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'
import { storage, errorUtils } from '../utils'
import { STORAGE_CONFIG, SUCCESS_MESSAGES } from '../config'

// Global reactive state
const user = ref(null)
const isAuthenticated = ref(false)
const isLoading = ref(false)
const error = ref(null)

/**
 * Authentication composable
 * @returns {object} Authentication state and methods
 */
export function useAuth() {
  const router = useRouter()

  // Computed properties
  const userData = computed(() => user.value)
  const isLoggedIn = computed(() => isAuthenticated.value)
  const loading = computed(() => isLoading.value)
  const authError = computed(() => error.value)

  /**
   * Initialize authentication state from localStorage
   */
  const initializeAuth = () => {
    try {
      const token = storage.getItem(STORAGE_CONFIG.KEYS.ACCESS_TOKEN)
      const userData = storage.getItem(STORAGE_CONFIG.KEYS.USER_DATA)

      if (token && userData) {
        user.value = userData
        isAuthenticated.value = true
      }
    } catch (err) {
      errorUtils.logError(err, 'initializeAuth')
      clearAuth()
    }
  }

  /**
   * Login user
   * @param {string} username - Username
   * @param {string} password - Password
   * @returns {Promise<boolean>} - Success status
   */
  const login = async (username, password) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await authAPI.login(username, password)
      
      // Store authentication data
      storage.setItem(
        STORAGE_CONFIG.KEYS.ACCESS_TOKEN, 
        response.access_token,
        STORAGE_CONFIG.EXPIRY.TOKEN
      )
      
      const userData = {
        user_id: response.user_id,
        username: response.username,
        first_name: response.first_name,
        last_name: response.last_name
      }
      
      storage.setItem(
        STORAGE_CONFIG.KEYS.USER_DATA, 
        userData,
        STORAGE_CONFIG.EXPIRY.USER_DATA
      )

      // Update state
      user.value = userData
      isAuthenticated.value = true

      return true
    } catch (err) {
      error.value = errorUtils.getErrorMessage(err)
      errorUtils.logError(err, 'login')
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout user
   */
  const logout = () => {
    try {
      // Clear storage
      storage.clear()
      
      // Reset state
      user.value = null
      isAuthenticated.value = false
      error.value = null

      // Redirect to login
      router.push('/login')
    } catch (err) {
      errorUtils.logError(err, 'logout')
    }
  }

  /**
   * Clear authentication data
   */
  const clearAuth = () => {
    storage.clear()
    user.value = null
    isAuthenticated.value = false
    error.value = null
  }

  /**
   * Check if user has valid session
   * @returns {boolean} - Is session valid
   */
  const hasValidSession = () => {
    const token = storage.getItem(STORAGE_CONFIG.KEYS.ACCESS_TOKEN)
    const userData = storage.getItem(STORAGE_CONFIG.KEYS.USER_DATA)
    return !!(token && userData)
  }

  /**
   * Refresh user data
   * @returns {Promise<boolean>} - Success status
   */
  const refreshUserData = async () => {
    if (!isAuthenticated.value) return false

    try {
      // In a real app, you might call an API to refresh user data
      const userData = storage.getItem(STORAGE_CONFIG.KEYS.USER_DATA)
      if (userData) {
        user.value = userData
        return true
      }
      return false
    } catch (err) {
      errorUtils.logError(err, 'refreshUserData')
      return false
    }
  }

  /**
   * Handle authentication errors
   * @param {Error} err - Error object
   */
  const handleAuthError = (err) => {
    if (err.response?.status === 401) {
      clearAuth()
      router.push('/login')
    }
    error.value = errorUtils.getErrorMessage(err)
  }

  return {
    // State
    userData,
    isLoggedIn,
    loading,
    authError,
    
    // Methods
    initializeAuth,
    login,
    logout,
    clearAuth,
    hasValidSession,
    refreshUserData,
    handleAuthError
  }
}

// Export global state for use in other composables
export { user, isAuthenticated, isLoading, error }
