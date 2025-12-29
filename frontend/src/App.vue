<template>
  <div>
    <h1>🏠 Home Energy Advisor</h1>
    <p class="subtitle">Get AI-powered energy efficiency recommendations for your home</p>

    <div class="container">
      <!-- Home Profile Form -->
      <HomeProfileForm 
        v-if="!advice"
        :loading="loading"
        :error="error"
        @submit="generateAdvice"
      />

      <!-- Loading State -->
      <LoadingSpinner 
        v-if="loading"
        message="Analyzing your home and generating personalized recommendations..."
        sub-message="This may take 10-30 seconds"
      />

      <!-- Results -->
      <AdviceResults 
        v-if="advice && !loading"
        :advice="advice"
        @reset="reset"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useEnergyAdvice } from './composables/useEnergyAdvice';
import HomeProfileForm from './components/home/HomeProfileForm.vue';
import LoadingSpinner from './components/common/LoadingSpinner.vue';
import AdviceResults from './components/advice/AdviceResults.vue';

const { loading, error, advice, generateAdvice, reset } = useEnergyAdvice();
</script>
