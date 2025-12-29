<template>
  <div class="loading">
    <div class="spinner"></div>
    <p>{{ message }}</p>
    <p v-if="subMessage" class="sub-message">{{ subMessage }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string;
  subMessage?: string;
}

withDefaults(defineProps<Props>(), {
  message: 'Loading...',
  subMessage: ''
});
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e8eaf6;
  border-top: 4px solid #5c6bc0;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 1.1rem;
}

.sub-message {
  font-size: 0.9rem;
  color: #888;
  margin-top: 0.5rem;
}
</style>
