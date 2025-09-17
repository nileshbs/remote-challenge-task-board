<template>
  <div class="card">
    <h1>{{ msg }}</h1>

    <div class="api-section">
      <h2>Backend API Status</h2>
      <button @click="fetchFromBackend" :disabled="loading">
        {{ loading ? 'Loading...' : 'Test Backend Connection' }}
      </button>
      
      <div v-if="backendMessage" class="response">
        <h3>Response from Backend:</h3>
        <pre>{{ JSON.stringify(backendMessage, null, 2) }}</pre>
      </div>
      
      <div v-if="error" class="error">
        <h3>Error:</h3>
        <p>{{ error }}</p>
        <p><small>Make sure the backend is running on http://10.0.0.8:8000</small></p>
      </div>
    </div>

    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>

    <p>
      Check out
      <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
        >create-vue</a
      >, the official Vue + Vite starter
    </p>
    <p>
      Install
      <a href="https://github.com/vuejs/language-tools" target="_blank">Volar</a>
      in your IDE for a better DX
    </p>
    <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

defineProps({
  msg: String,
})

const backendMessage = ref(null)
const error = ref(null)
const loading = ref(false)

const fetchFromBackend = async () => {
  loading.value = true
  error.value = null
  backendMessage.value = null
  
  try {
    const response = await axios.get('http://10.0.0.8:8000/api/hello')
    backendMessage.value = response.data
  } catch (err) {
    error.value = err.message
    console.error('Error fetching from backend:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}

.api-section {
  margin: 2em 0;
  padding: 1.5em;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.05);
}

.response {
  margin-top: 1em;
  text-align: left;
}

.response pre {
  background-color: #f5f5f5;
  color: #333;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
}

.error {
  margin-top: 1em;
  color: #ff6b6b;
}

.error p {
  margin: 0.5em 0;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (prefers-color-scheme: light) {
  .response pre {
    background-color: #f5f5f5;
    color: #333;
  }
}

@media (prefers-color-scheme: dark) {
  .response pre {
    background-color: #1a1a1a;
    color: #fff;
  }
}</style>
