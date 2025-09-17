<template>
  <div class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-container" @click.stop>
      <div class="dialog-header">
        <h2>Add New Task</h2>
        <button @click="$emit('close')" class="close-button">×</button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="dialog-form">
        <div class="form-group">
          <label for="title">Title *</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            placeholder="Enter task title"
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="details">Details</label>
          <textarea
            id="details"
            v-model="form.details"
            placeholder="Enter task details"
            rows="4"
            :disabled="loading"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="due_date">Due Date *</label>
          <input
            id="due_date"
            v-model="form.due_date"
            type="date"
            required
            :disabled="loading"
          />
        </div>
        
        <div class="form-actions">
          <button type="button" @click="$emit('close')" :disabled="loading" class="cancel-button">
            Cancel
          </button>
          <button type="submit" :disabled="loading || !isFormValid" class="save-button">
            <span v-if="loading">Creating...</span>
            <span v-else>Create Task</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['close', 'save'])

const form = ref({
  title: '',
  details: '',
  due_date: ''
})

const loading = ref(false)

const isFormValid = computed(() => {
  return form.value.title.trim() && form.value.due_date
})

const handleSubmit = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  
  try {
    const taskData = {
      title: form.value.title.trim(),
      details: form.value.details.trim(),
      due_date: form.value.due_date,
      status: 'To Do'
    }
    
    emit('save', taskData)
  } catch (error) {
    console.error('Error creating task:', error)
  } finally {
    loading.value = false
  }
}

const handleOverlayClick = () => {
  if (!loading.value) {
    emit('close')
  }
}

// Set default due date to tomorrow
const tomorrow = new Date()
tomorrow.setDate(tomorrow.getDate() + 1)
form.value.due_date = tomorrow.toISOString().split('T')[0]
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.dialog-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.5rem 0 1.5rem;
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 1.5rem;
}

.dialog-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  background-color: #f8f9fa;
  color: #333;
}

.dialog-form {
  padding: 0 1.5rem 1.5rem 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled,
.form-group textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-button,
.save-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}

.cancel-button:hover:not(:disabled) {
  background-color: #5a6268;
}

.save-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.save-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.cancel-button:disabled,
.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.save-button:disabled {
  box-shadow: none;
}

@media (max-width: 600px) {
  .dialog-container {
    margin: 20px;
    max-width: none;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-button,
  .save-button {
    width: 100%;
  }
}
</style>
