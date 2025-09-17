<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">{{ APP_CONFIG.NAME }}</h1>
      <p class="login-subtitle">Sign in to manage your tasks</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            :disabled="loading"
            placeholder="Enter your username"
            autocomplete="username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            :disabled="loading"
            placeholder="Enter your password"
            autocomplete="current-password"
          />
        </div>
        
        <button type="submit" :disabled="loading || !isFormValid" class="login-button">
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
        
        <div v-if="authError" class="error-message">
          {{ authError }}
        </div>
      </form>
      
      <div class="demo-credentials">
        <h3>Demo Credentials:</h3>
        <p><strong>Username:</strong> johndoe</p>
        <p><strong>Password:</strong> password123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { useNotifications } from '../composables/useNotifications'
import { APP_CONFIG } from '../config'
import { validation } from '../utils'

const router = useRouter()

// Composables
const { login, loading, authError } = useAuth()
const { authNotifications } = useNotifications()

// Form state
const form = ref({
  username: '',
  password: ''
})

// Computed properties
const isFormValid = computed(() => {
  return validation.isRequired(form.value.username) && 
         validation.isRequired(form.value.password)
})

// Methods
const handleLogin = async () => {
  if (!isFormValid.value) return
  
  const success = await login(form.value.username, form.value.password)
  
  if (success) {
    authNotifications.loginSuccess()
    router.push('/taskboard')
  } else {
    authNotifications.loginError(authError.value)
  }
}

// Lifecycle
onMounted(() => {
  // Focus on username field
  const usernameInput = document.getElementById('username')
  if (usernameInput) {
    usernameInput.focus()
  }
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-title {
  text-align: center;
  color: #333;
  margin-bottom: 8px;
  font-size: 2rem;
  font-weight: 700;
}

.login-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 32px;
  font-size: 1rem;
}

.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  text-align: center;
  border: 1px solid #fcc;
}

.demo-credentials {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.demo-credentials h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 0.9rem;
}

.demo-credentials p {
  margin: 4px 0;
  color: #666;
  font-size: 0.85rem;
}
</style>

