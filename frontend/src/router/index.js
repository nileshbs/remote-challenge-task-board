/**
 * Vue Router configuration
 * Following Single Responsibility Principle (SRP)
 * Provides routing with authentication guards
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { APP_CONFIG } from '../config'

// Route imports
import Login from '../views/Login.vue'
import TaskBoard from '../views/TaskBoard.vue'

// Route definitions
const routes = [
  {
    path: '/',
    redirect: APP_CONFIG.ROUTES.LOGIN
  },
  {
    path: APP_CONFIG.ROUTES.LOGIN,
    name: 'Login',
    component: Login,
    meta: { 
      requiresGuest: true,
      title: 'Login - Task Manager'
    }
  },
  {
    path: APP_CONFIG.ROUTES.TASKBOARD,
    name: 'TaskBoard',
    component: TaskBoard,
    meta: { 
      requiresAuth: true,
      title: 'Task Board - Task Manager'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/'
  }
]

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Return to saved position or top of page
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const { hasValidSession } = useAuth()
  
  // Check authentication status
  const isAuthenticated = hasValidSession()
  
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Handle authentication requirements
  if (to.meta.requiresAuth && !isAuthenticated) {
    next(APP_CONFIG.ROUTES.LOGIN)
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next(APP_CONFIG.ROUTES.TASKBOARD)
  } else {
    next()
  }
})

// Global after hook for analytics or logging
router.afterEach((to, from) => {
  // Log route changes in development
  if (process.env.NODE_ENV === 'development') {
    console.log(`Route changed from ${from.path} to ${to.path}`)
  }
  
  // In production, you might want to send analytics events here
  // analytics.track('page_view', { path: to.path, name: to.name })
})

export default router
