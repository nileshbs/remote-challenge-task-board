<template>
  <div 
    class="delete-zone"
    :class="zoneClasses"
    @drop="handleDrop"
    @dragover.prevent
    @dragenter="handleDragEnter"
    @dragleave="handleDragLeave"
  >
    <div class="delete-icon">🗑️</div>
    <p>Drop here to delete</p>
  </div>
</template>

<script setup>

import { computed } from 'vue'

// Props
const props = defineProps({
  dragOver: {
    type: Boolean,
    default: false
  },
  canDrop: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['drop', 'drag-enter', 'drag-leave'])

// Computed
const zoneClasses = computed(() => ({
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
.delete-zone {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #dc3545;
  color: white;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
  transition: all 0.3s ease;
  z-index: 1000;
  opacity: 0.8;
}

.delete-zone.drag-over {
  transform: scale(1.1);
  background: #c82333;
  opacity: 1;
}

.delete-zone.can-drop {
  opacity: 1;
  box-shadow: 0 6px 20px rgba(220, 53, 69, 0.5);
}

.delete-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.delete-zone p {
  margin: 0;
  font-weight: 600;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .delete-zone {
    bottom: 1rem;
    right: 1rem;
    padding: 0.75rem;
  }
  
  .delete-icon {
    font-size: 1.5rem;
  }
  
  .delete-zone p {
    font-size: 0.8rem;
  }
}
</style>
