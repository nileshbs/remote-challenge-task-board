<template>
  <header class="taskboard-header">
    <div class="header-content">
      <h1 class="app-title">Task Board</h1>
      <div class="user-info">
        <span class="welcome-text">Welcome, {{ userData?.first_name }}!</span>
        <button 
          @click="$emit('logout')" 
          class="logout-button"
          :disabled="loading"
        >
          Logout
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuth } from '../composables/useAuth'

// Props
defineProps({
  userData: {
    type: Object,
    default: null
  }
})

// Emits
defineEmits(['logout'])

// Composables
const { loading } = useAuth()
</script>

<style scoped>
.taskboard-header {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  color: #333;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-text {
  color: #666;
  font-weight: 500;
}

.logout-button {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.logout-button:hover:not(:disabled) {
  background: #c82333;
}

.logout-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
