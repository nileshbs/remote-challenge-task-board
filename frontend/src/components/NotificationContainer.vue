<template>
  <div class="notification-container">
    <TransitionGroup name="notification" tag="div">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification"
        :class="notificationClasses(notification.type)"
        @click="removeNotification(notification.id)"
      >
        <div class="notification-content">
          <div class="notification-icon">
            <span v-if="notification.type === 'success'">✅</span>
            <span v-else-if="notification.type === 'error'">❌</span>
            <span v-else-if="notification.type === 'warning'">⚠️</span>
            <span v-else>ℹ️</span>
          </div>
          <div class="notification-message">
            {{ notification.message }}
          </div>
          <button 
            v-if="notification.closable"
            class="notification-close"
            @click.stop="removeNotification(notification.id)"
          >
            ×
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useNotifications } from '../composables/useNotifications'

// Composables
const { notifications, removeNotification } = useNotifications()

// Methods
const notificationClasses = (type) => ({
  [`notification-${type}`]: true
})
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 3000;
  max-width: 400px;
}

.notification {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 4px solid;
}

.notification:hover {
  transform: translateX(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.notification-success {
  border-left-color: #28a745;
}

.notification-error {
  border-left-color: #dc3545;
}

.notification-warning {
  border-left-color: #fd7e14;
}

.notification-info {
  border-left-color: #17a2b8;
}

.notification-content {
  display: flex;
  align-items: center;
  padding: 1rem;
  gap: 0.75rem;
}

.notification-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.notification-message {
  flex: 1;
  color: #333;
  font-weight: 500;
  line-height: 1.4;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.notification-close:hover {
  background: #f8f9fa;
  color: #666;
}

/* Transition animations */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}

@media (max-width: 768px) {
  .notification-container {
    top: 0.5rem;
    right: 0.5rem;
    left: 0.5rem;
    max-width: none;
  }
  
  .notification-content {
    padding: 0.75rem;
  }
  
  .notification-message {
    font-size: 0.9rem;
  }
}
</style>
