<template>
  <div class="taskboard-container">
    <!-- Header -->
    <TaskBoardHeader 
      :user-data="userData" 
      @logout="handleLogout" 
    />

    <!-- Main Content -->
    <main class="taskboard-main">
      <!-- Search and Add Task Section -->
      <div class="search-add-section">
        <!-- Search Bar -->
        <div class="search-container">
          <div class="search-input-wrapper">
            <span class="search-icon">🔍</span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search tasks by title or details... (Ctrl+K to focus)"
              class="search-input"
              :disabled="loading"
              ref="searchInput"
              @keydown.escape="clearSearch"
            />
            <button
              v-if="searchQuery"
              @click="clearSearch"
              class="clear-search-button"
              title="Clear search"
            >
              ✕
            </button>
          </div>
          <div v-if="searchQuery" class="search-results-info">
            <span v-if="filteredTasksCount > 0">
              {{ filteredTasksCount }} of {{ allTasks.length }} tasks match "{{ searchQuery }}"
            </span>
            <span v-else class="no-results">
              No tasks match "{{ searchQuery }}"
            </span>
          </div>
        </div>

        <!-- Add Task Button -->
        <button 
          @click="showAddTaskDialog = true" 
          class="add-task-button"
          :disabled="loading"
        >
          <span class="plus-icon">+</span>
          Add New Task
        </button>
      </div>

      <!-- Task Columns -->
      <div class="taskboard-columns">
        <TaskColumn
          v-for="status in TASK_CONFIG.VALID_STATUSES"
          :key="status"
          :status="status"
          :tasks="getFilteredTasksByStatus(status)"
          :search-query="searchQuery"
          :drag-over="dragOverColumn === status"
          :can-drop="canDropOnStatus(draggedTask?.status, status)"
          @drop="handleColumnDrop($event, status)"
          @drag-enter="handleDragEnter($event, status)"
          @drag-leave="handleDragLeave"
          @edit-task="handleEditTask"
          @delete-task="handleDeleteTask"
        />
      </div>

      <!-- Delete Zone -->
      <DeleteZone
        :drag-over="dragOverDelete"
        :can-drop="isDragging"
        @drop="handleDeleteDrop"
        @drag-enter="handleDeleteDragEnter"
        @drag-leave="handleDragLeave"
      />
    </main>

    <!-- Dialogs -->
    <AddTaskDialog
      v-if="showAddTaskDialog"
      @close="showAddTaskDialog = false"
      @save="handleAddTask"
    />

    <EditTaskDialog
      v-if="showEditTaskDialog && selectedTask"
      :task="selectedTask"
      @close="showEditTaskDialog = false"
      @save="handleUpdateTask"
    />

    <!-- Loading Overlay -->
    <LoadingOverlay v-if="loading" />

    <!-- Notifications -->
    <NotificationContainer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

// Composables
import { useAuth } from '../composables/useAuth'
import { useTasks } from '../composables/useTasks'
import { useDragDrop } from '../composables/useDragDrop'
import { useNotifications } from '../composables/useNotifications'

// Utils
import { searchUtils } from '../utils'

// Components
import TaskBoardHeader from '../components/TaskBoardHeader.vue'
import TaskColumn from '../components/TaskColumn.vue'
import DeleteZone from '../components/DeleteZone.vue'
import AddTaskDialog from '../components/AddTaskDialog.vue'
import EditTaskDialog from '../components/EditTaskDialog.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'
import NotificationContainer from '../components/NotificationContainer.vue'

// Configuration
import { TASK_CONFIG } from '../config'

const router = useRouter()

// Composables
const { userData, logout } = useAuth()
const { 
  allTasks, 
  loading, 
  tasksError, 
  currentTask,
  getTasksByStatus,
  loadTasks,
  createTask,
  updateTask,
  deleteTask,
  moveTask,
  setSelectedTask,
  clearSelectedTask
} = useTasks()

const {
  dragOverColumn,
  dragOverDelete,
  isDragging,
  draggedTask,
  handleDragEnter,
  handleDeleteDragEnter,
  handleDragLeave,
  canDropOnStatus
} = useDragDrop()

const { taskNotifications, showError } = useNotifications()

// Local state
const showAddTaskDialog = ref(false)
const showEditTaskDialog = ref(false)
const searchQuery = ref('')
const searchInput = ref(null)

// Computed properties
const selectedTask = computed(() => currentTask.value)

// Filtered tasks based on search query
const filteredTasks = computed(() => {
  return searchUtils.filterTasks(allTasks.value, searchQuery.value)
})

// Filtered tasks count
const filteredTasksCount = computed(() => filteredTasks.value.length)

// Get filtered tasks by status
const getFilteredTasksByStatus = (status) => {
  return filteredTasks.value.filter(task => task.status === status)
}

// Methods
const handleAddTask = async (taskData) => {
  const success = await createTask(taskData)
  if (success) {
    showAddTaskDialog.value = false
    taskNotifications.created()
  } else {
    showError(tasksError.value || 'Failed to create task')
  }
}

const handleEditTask = (task) => {
  setSelectedTask(task)
  showEditTaskDialog.value = true
}

const handleUpdateTask = async (taskId, updateData) => {
  const success = await updateTask(taskId, updateData)
  if (success) {
    showEditTaskDialog.value = false
    clearSelectedTask()
    taskNotifications.updated()
  } else {
    showError(tasksError.value || 'Failed to update task')
  }
}

const handleDeleteTask = async (taskId) => {
  if (confirm('Are you sure you want to delete this task?')) {
    const success = await deleteTask(taskId)
    if (success) {
      taskNotifications.deleted()
    } else {
      showError(tasksError.value || 'Failed to delete task')
    }
  }
}

const handleLogout = () => {
  logout()
}

const clearSearch = () => {
  searchQuery.value = ''
}

// Enhanced drag and drop handlers
const handleColumnDrop = async (event, newStatus) => {
  event.preventDefault()
  dragOverColumn.value = null
  
  const taskId = event.dataTransfer.getData('text/plain')
  
  if (taskId && TASK_CONFIG.VALID_STATUSES.includes(newStatus)) {
    const success = await moveTask(taskId, newStatus)
    if (success) {
      taskNotifications.moved()
    } else {
      showError(tasksError.value || 'Failed to move task')
    }
  }
}

const handleDeleteDrop = async (event) => {
  event.preventDefault()
  dragOverDelete.value = false
  
  const taskId = event.dataTransfer.getData('text/plain')
  
  if (taskId) {
    await handleDeleteTask(taskId)
  }
}

// Keyboard shortcuts
const handleKeydown = (event) => {
  // Ctrl+K or Cmd+K to focus search
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault()
    if (searchInput.value) {
      searchInput.value.focus()
    }
  }
}

// Lifecycle
onMounted(async () => {
  const success = await loadTasks()
  if (!success && tasksError.value) {
    showError(tasksError.value)
  }
  
  // Add keyboard event listener
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  // Remove keyboard event listener
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.taskboard-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.taskboard-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-add-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.search-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input-wrapper:focus-within {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-icon {
  font-size: 1.1rem;
  color: #666;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  color: #333;
  background: transparent;
}

.search-input::placeholder {
  color: #999;
}

.search-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.clear-search-button {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.2s;
  flex-shrink: 0;
}

.clear-search-button:hover {
  background: #f8f9fa;
  color: #666;
}

.search-results-info {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
  padding-left: 0.5rem;
}

.search-results-info .no-results {
  color: #dc3545;
  font-weight: 500;
}

.add-task-section {
  display: flex;
  justify-content: flex-end;
}

.add-task-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.2s;
}

.add-task-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.add-task-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.plus-icon {
  font-size: 1.2rem;
}

.taskboard-columns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

@media (max-width: 768px) {
  .taskboard-columns {
    grid-template-columns: 1fr;
  }
  
  .taskboard-main {
    padding: 1rem;
  }
  
  .search-add-section {
    gap: 1rem;
  }
  
  .search-input-wrapper {
    padding: 0.5rem 0.75rem;
  }
  
  .search-input {
    font-size: 0.9rem;
  }
  
  .add-task-section {
    justify-content: stretch;
  }
  
  .add-task-button {
    width: 100%;
    justify-content: center;
  }
}
</style>