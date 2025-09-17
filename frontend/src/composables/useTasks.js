/**
 * Tasks composable
 * Following Single Responsibility Principle (SRP)
 * Provides task management state and methods
 */

import { ref, computed } from 'vue'
import { tasksAPI } from '../services/api'
import { errorUtils } from '../utils'
import { TASK_CONFIG, SUCCESS_MESSAGES } from '../config'

// Global reactive state
const tasks = ref([])
const isLoading = ref(false)
const error = ref(null)
const selectedTask = ref(null)

/**
 * Tasks composable
 * @returns {object} Tasks state and methods
 */
export function useTasks() {
  // Computed properties
  const allTasks = computed(() => tasks.value)
  const loading = computed(() => isLoading.value)
  const tasksError = computed(() => error.value)
  const currentTask = computed(() => selectedTask.value)

  /**
   * Get tasks grouped by status
   */
  const tasksByStatus = computed(() => {
    return TASK_CONFIG.VALID_STATUSES.reduce((acc, status) => {
      acc[status] = tasks.value.filter(task => task.status === status)
      return acc
    }, {})
  })

  /**
   * Get task counts by status
   */
  const taskCounts = computed(() => {
    return TASK_CONFIG.VALID_STATUSES.reduce((acc, status) => {
      acc[status] = tasks.value.filter(task => task.status === status).length
      return acc
    }, {})
  })

  /**
   * Get tasks by specific status
   * @param {string} status - Task status
   * @returns {Array} - Tasks with the specified status
   */
  const getTasksByStatus = (status) => {
    return tasks.value.filter(task => task.status === status)
  }

  /**
   * Load all tasks
   * @returns {Promise<boolean>} - Success status
   */
  const loadTasks = async () => {
    isLoading.value = true
    error.value = null

    try {
      const response = await tasksAPI.getTasks()
      tasks.value = response.tasks || []
      return true
    } catch (err) {
      error.value = errorUtils.getErrorMessage(err)
      errorUtils.logError(err, 'loadTasks')
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Create a new task
   * @param {object} taskData - Task data
   * @returns {Promise<boolean>} - Success status
   */
  const createTask = async (taskData) => {
    isLoading.value = true
    error.value = null

    try {
      const newTask = await tasksAPI.createTask(taskData)
      tasks.value.push(newTask)
      return true
    } catch (err) {
      error.value = errorUtils.getErrorMessage(err)
      errorUtils.logError(err, 'createTask')
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Update an existing task
   * @param {string} taskId - Task ID
   * @param {object} updateData - Update data
   * @returns {Promise<boolean>} - Success status
   */
  const updateTask = async (taskId, updateData) => {
    isLoading.value = true
    error.value = null

    try {
      const updatedTask = await tasksAPI.updateTask(taskId, updateData)
      const index = tasks.value.findIndex(task => task.task_id === taskId)
      
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
      
      return true
    } catch (err) {
      error.value = errorUtils.getErrorMessage(err)
      errorUtils.logError(err, 'updateTask')
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Delete a task
   * @param {string} taskId - Task ID
   * @returns {Promise<boolean>} - Success status
   */
  const deleteTask = async (taskId) => {
    isLoading.value = true
    error.value = null

    try {
      await tasksAPI.deleteTask(taskId)
      tasks.value = tasks.value.filter(task => task.task_id !== taskId)
      return true
    } catch (err) {
      error.value = errorUtils.getErrorMessage(err)
      errorUtils.logError(err, 'deleteTask')
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Move task to different status
   * @param {string} taskId - Task ID
   * @param {string} newStatus - New status
   * @returns {Promise<boolean>} - Success status
   */
  const moveTask = async (taskId, newStatus) => {
    if (!TASK_CONFIG.VALID_STATUSES.includes(newStatus)) {
      error.value = 'Invalid task status'
      return false
    }

    const task = tasks.value.find(t => t.task_id === taskId)
    if (!task || task.status === newStatus) {
      return true // No change needed
    }

    return await updateTask(taskId, { status: newStatus })
  }

  /**
   * Get task by ID
   * @param {string} taskId - Task ID
   * @returns {object|null} - Task object or null
   */
  const getTaskById = (taskId) => {
    return tasks.value.find(task => task.task_id === taskId) || null
  }

  /**
   * Set selected task
   * @param {object|null} task - Task to select
   */
  const setSelectedTask = (task) => {
    selectedTask.value = task
  }

  /**
   * Clear selected task
   */
  const clearSelectedTask = () => {
    selectedTask.value = null
  }

  /**
   * Clear all tasks
   */
  const clearTasks = () => {
    tasks.value = []
    selectedTask.value = null
    error.value = null
  }

  /**
   * Refresh tasks from server
   * @returns {Promise<boolean>} - Success status
   */
  const refreshTasks = async () => {
    return await loadTasks()
  }

  /**
   * Get task statistics
   * @returns {object} - Task statistics
   */
  const getTaskStats = () => {
    const total = tasks.value.length
    const completed = taskCounts.value[TASK_CONFIG.STATUSES.COMPLETED]
    const inProgress = taskCounts.value[TASK_CONFIG.STATUSES.IN_PROGRESS]
    const todo = taskCounts.value[TASK_CONFIG.STATUSES.TODO]

    return {
      total,
      completed,
      inProgress,
      todo,
      completionRate: total > 0 ? Math.round((completed / total) * 100) : 0
    }
  }

  return {
    // State
    allTasks,
    loading,
    tasksError,
    currentTask,
    tasksByStatus,
    taskCounts,
    
    // Methods
    getTasksByStatus,
    loadTasks,
    createTask,
    updateTask,
    deleteTask,
    moveTask,
    getTaskById,
    setSelectedTask,
    clearSelectedTask,
    clearTasks,
    refreshTasks,
    getTaskStats
  }
}

// Export global state for use in other composables
export { tasks, isLoading, error, selectedTask }
