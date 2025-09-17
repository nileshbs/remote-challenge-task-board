/**
 * Drag and Drop composable
 * Following Single Responsibility Principle (SRP)
 * Provides drag and drop functionality for tasks
 */

import { ref, onMounted, onUnmounted } from 'vue'
import { useTasks } from './useTasks'
import { TASK_CONFIG } from '../config'

/**
 * Drag and Drop composable
 * @returns {object} Drag and drop state and methods
 */
export function useDragDrop() {
  const { moveTask } = useTasks()

  // Reactive state
  const dragOverColumn = ref(null)
  const dragOverDelete = ref(false)
  const isDragging = ref(false)
  const draggedTask = ref(null)

  /**
   * Handle drag start
   * @param {DragEvent} event - Drag event
   * @param {object} task - Task being dragged
   */
  const handleDragStart = (event, task) => {
    isDragging.value = true
    draggedTask.value = task
    
    // Set drag data
    event.dataTransfer.setData('text/plain', task.task_id)
    event.dataTransfer.effectAllowed = 'move'
    
    // Add visual feedback
    if (event.target) {
      event.target.style.opacity = '0.5'
    }
  }

  /**
   * Handle drag end
   * @param {DragEvent} event - Drag event
   */
  const handleDragEnd = (event) => {
    isDragging.value = false
    draggedTask.value = null
    
    // Remove visual feedback
    if (event.target) {
      event.target.style.opacity = '1'
    }
    
    // Clear drag over states
    dragOverColumn.value = null
    dragOverDelete.value = false
  }

  /**
   * Handle drag over
   * @param {DragEvent} event - Drag event
   */
  const handleDragOver = (event) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }

  /**
   * Handle drag enter for columns
   * @param {DragEvent} event - Drag event
   * @param {string} status - Column status
   */
  const handleDragEnter = (event, status) => {
    event.preventDefault()
    if (TASK_CONFIG.VALID_STATUSES.includes(status)) {
      dragOverColumn.value = status
    }
  }

  /**
   * Handle drag enter for delete zone
   * @param {DragEvent} event - Drag event
   */
  const handleDeleteDragEnter = (event) => {
    event.preventDefault()
    dragOverDelete.value = true
  }

  /**
   * Handle drag leave
   * @param {DragEvent} event - Drag event
   */
  const handleDragLeave = (event) => {
    // Only clear if we're leaving the drop zone entirely
    const rect = event.currentTarget.getBoundingClientRect()
    const x = event.clientX
    const y = event.clientY
    
    if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
      dragOverColumn.value = null
      dragOverDelete.value = false
    }
  }

  /**
   * Handle drop on column
   * @param {DragEvent} event - Drag event
   * @param {string} newStatus - New status for the task
   */
  const handleColumnDrop = async (event, newStatus) => {
    event.preventDefault()
    dragOverColumn.value = null
    
    const taskId = event.dataTransfer.getData('text/plain')
    
    if (taskId && TASK_CONFIG.VALID_STATUSES.includes(newStatus)) {
      await moveTask(taskId, newStatus)
    }
  }

  /**
   * Handle drop on delete zone
   * @param {DragEvent} event - Drag event
   * @param {Function} onDelete - Delete callback function
   */
  const handleDeleteDrop = async (event, onDelete) => {
    event.preventDefault()
    dragOverDelete.value = false
    
    const taskId = event.dataTransfer.getData('text/plain')
    
    if (taskId && typeof onDelete === 'function') {
      await onDelete(taskId)
    }
  }

  /**
   * Check if task can be dropped on status
   * @param {string} currentStatus - Current task status
   * @param {string} targetStatus - Target status
   * @returns {boolean} - Can drop
   */
  const canDropOnStatus = (currentStatus, targetStatus) => {
    return currentStatus !== targetStatus && TASK_CONFIG.VALID_STATUSES.includes(targetStatus)
  }

  /**
   * Get drop zone class
   * @param {string} status - Column status
   * @returns {string} - CSS class
   */
  const getDropZoneClass = (status) => {
    return {
      'drag-over': dragOverColumn.value === status,
      'can-drop': isDragging.value && canDropOnStatus(draggedTask.value?.status, status)
    }
  }

  /**
   * Get delete zone class
   * @returns {string} - CSS class
   */
  const getDeleteZoneClass = () => {
    return {
      'drag-over': dragOverDelete.value,
      'can-drop': isDragging.value
    }
  }

  /**
   * Clear all drag states
   */
  const clearDragStates = () => {
    dragOverColumn.value = null
    dragOverDelete.value = false
    isDragging.value = false
    draggedTask.value = null
  }

  /**
   * Setup global drag and drop event listeners
   */
  const setupGlobalListeners = () => {
    // Prevent default drag behavior on images and links
    document.addEventListener('dragstart', (event) => {
      if (event.target.tagName === 'IMG' || event.target.tagName === 'A') {
        event.preventDefault()
      }
    })

    // Clear drag states when drag ends globally
    document.addEventListener('dragend', clearDragStates)
  }

  /**
   * Cleanup global event listeners
   */
  const cleanupGlobalListeners = () => {
    document.removeEventListener('dragstart', (event) => {
      if (event.target.tagName === 'IMG' || event.target.tagName === 'A') {
        event.preventDefault()
      }
    })
    document.removeEventListener('dragend', clearDragStates)
  }

  // Setup and cleanup
  onMounted(() => {
    setupGlobalListeners()
  })

  onUnmounted(() => {
    cleanupGlobalListeners()
  })

  return {
    // State
    dragOverColumn,
    dragOverDelete,
    isDragging,
    draggedTask,
    
    // Methods
    handleDragStart,
    handleDragEnd,
    handleDragOver,
    handleDragEnter,
    handleDeleteDragEnter,
    handleDragLeave,
    handleColumnDrop,
    handleDeleteDrop,
    canDropOnStatus,
    getDropZoneClass,
    getDeleteZoneClass,
    clearDragStates
  }
}
