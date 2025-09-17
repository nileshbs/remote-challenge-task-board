<template>
  <div 
    class="task-column"
    :class="columnClasses"
  >
    <div class="column-header">
      <h3>{{ status }}</h3>
      <span class="task-count">{{ tasks.length }}</span>
    </div>
    <div 
      class="column-content"
      @drop="handleDrop"
      @dragover.prevent
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
    >
      <TaskCard
        v-for="task in tasks"
        :key="task.task_id"
        :task="task"
        @edit="$emit('edit-task', task)"
        @delete="$emit('delete-task', task.task_id)"
      />
      
      <!-- Empty state -->
      <div v-if="tasks.length === 0" class="empty-state">
        <p v-if="!searchQuery">No tasks in {{ status }}</p>
        <p v-else>No tasks in {{ status }} match "{{ searchQuery }}"</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import TaskCard from './TaskCard.vue'

// Props
const props = defineProps({
  status: {
    type: String,
    required: true
  },
  tasks: {
    type: Array,
    default: () => []
  },
  dragOver: {
    type: Boolean,
    default: false
  },
  canDrop: {
    type: Boolean,
    default: false
  },
  searchQuery: {
    type: String,
    default: ''
  }
})

// Emits
const emit = defineEmits(['drop', 'drag-enter', 'drag-leave', 'edit-task', 'delete-task'])

// Computed
const columnClasses = computed(() => ({
  'drag-over': props.dragOver,
  'can-drop': props.canDrop
}))

// Methods
const handleDrop = (event) => {
  emit('drop', event)
}

const handleDragEnter = (event) => {
  emit('drag-enter', event)
}

const handleDragLeave = (event) => {
  emit('drag-leave', event)
}
</script>

<style scoped>
.task-column {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.task-column.drag-over {
  border: 2px dashed #667eea;
  background-color: #f0f4ff;
}

.task-column.can-drop {
  border-color: #28a745;
  background-color: #f0fff4;
}

.column-header {
  background: #f8f9fa;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.column-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
  font-weight: 600;
}

.task-count {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.column-content {
  padding: 1rem;
  min-height: 400px;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #999;
  font-style: italic;
}

.empty-state p {
  margin: 0;
}
</style>
