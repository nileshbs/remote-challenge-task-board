<template>
  <div 
    class="task-card"
    :draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
  >
    <div class="task-header">
      <h4 class="task-title">{{ task.title }}</h4>
      <div class="task-actions">
        <button 
          @click="$emit('edit', task)" 
          class="edit-button" 
          title="Edit task"
          :disabled="isDragging"
        >
          ✏️
        </button>
        <button 
          @click="$emit('delete', task.task_id)" 
          class="delete-button" 
          title="Delete task"
          :disabled="isDragging"
        >
          🗑️
        </button>
      </div>
    </div>
    
    <div class="task-details">
      <p class="task-description">{{ task.details }}</p>
    </div>
    
    <div class="task-footer">
      <div class="task-due-date">
        <span class="date-label">Due:</span>
        <span class="date-value" :class="dateUtils.getDateClass(task.due_date)">
          {{ dateUtils.formatDisplayDate(task.due_date) }}
        </span>
      </div>
      <div class="task-status">
        <span class="status-badge" :class="getStatusClass(task.status)">
          {{ task.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { dateUtils } from '../utils'
import { TASK_CONFIG } from '../config'

// Props validation
const props = defineProps({
  task: {
    type: Object,
    required: true,
    validator: (value) => {
      return value && 
             typeof value.task_id === 'string' &&
             typeof value.title === 'string' &&
             typeof value.status === 'string' &&
             TASK_CONFIG.VALID_STATUSES.includes(value.status)
    }
  }
})

// Emits
defineEmits(['edit', 'delete'])

// Local state
const isDragging = ref(false)

// Methods
const handleDragStart = (event) => {
  isDragging.value = true
  event.dataTransfer.setData('text/plain', props.task.task_id)
  event.dataTransfer.effectAllowed = 'move'
  
  // Add visual feedback
  if (event.target) {
    event.target.style.opacity = '0.5'
  }
}

const handleDragEnd = (event) => {
  isDragging.value = false
  if (event.target) {
    event.target.style.opacity = '1'
  }
}

const getStatusClass = (status) => {
  const statusMap = {
    [TASK_CONFIG.STATUSES.TODO]: 'status-todo',
    [TASK_CONFIG.STATUSES.IN_PROGRESS]: 'status-progress',
    [TASK_CONFIG.STATUSES.COMPLETED]: 'status-completed'
  }
  
  return statusMap[status] || 'status-default'
}
</script>

<style scoped>
.task-card {
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  cursor: grab;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.task-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.task-card:active {
  cursor: grabbing;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.task-title {
  margin: 0;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.3;
  flex: 1;
  margin-right: 0.5rem;
}

.task-actions {
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.task-card:hover .task-actions {
  opacity: 1;
}

.edit-button,
.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.edit-button:hover {
  background-color: #e3f2fd;
}

.delete-button:hover {
  background-color: #ffebee;
}

.task-details {
  margin-bottom: 1rem;
}

.task-description {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}

.task-due-date {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.date-label {
  color: #999;
  font-weight: 500;
}

.date-value {
  font-weight: 600;
}

.date-value.overdue {
  color: #dc3545;
}

.date-value.due-soon {
  color: #fd7e14;
}

.date-value.due-normal {
  color: #28a745;
}

.task-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-todo {
  background-color: #e9ecef;
  color: #6c757d;
}

.status-progress {
  background-color: #fff3cd;
  color: #856404;
}

.status-completed {
  background-color: #d4edda;
  color: #155724;
}

.status-default {
  background-color: #f8f9fa;
  color: #495057;
}

/* Drag and drop styles */
.task-card[draggable="true"] {
  user-select: none;
}

.task-card.dragging {
  opacity: 0.5;
  transform: rotate(5deg);
}
</style>
