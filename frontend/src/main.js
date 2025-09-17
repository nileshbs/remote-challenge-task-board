/**
 * Main application entry point
 * Following Single Responsibility Principle (SRP)
 * Initializes the Vue application with all necessary plugins and configurations
 */

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { useAuth } from './composables/useAuth'

// Create Vue app instance
const app = createApp(App)

// Use plugins
app.use(router)

// Initialize authentication state
const { initializeAuth } = useAuth()
initializeAuth()

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err, info)
  
  // In production, you might want to send errors to a logging service
  if (process.env.NODE_ENV === 'production') {
    // errorTrackingService.captureException(err, { context: info })
  }
}

// Global warning handler
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Vue warning:', msg, trace)
}

// Mount the application
app.mount('#app')
