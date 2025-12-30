<template>
  <form @submit.prevent="handleSubmit">
    <h2>Tell us about your home</h2>
    
    <!-- Basic Information Section -->
    <BasicInfoSection v-model="formData" />

    <!-- Advanced Options Section -->
    <AdvancedSections
      v-model="formData"
      :show-advanced="showAdvanced"
      @toggle="showAdvanced = !showAdvanced"
    />

    <div v-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <div class="error-content">
        <div class="error-title">Unable to Generate Recommendations</div>
        <div class="error-message">{{ error }}</div>
        <div class="error-hint">Please try again or contact support if the problem persists.</div>
      </div>
    </div>

    <button type="submit" :disabled="loading" class="submit-btn">
      {{ loading ? 'Generating Recommendations...' : 'Get Energy Recommendations' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import BasicInfoSection from './BasicInfoSection.vue';
import AdvancedSections from './AdvancedSections.vue';
import type { HomeProfile } from '../../types';

interface Props {
  loading: boolean;
  error: string;
}

interface Emits {
  (e: 'submit', formData: HomeProfile): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

const showAdvanced = ref(false);

const formData = reactive<HomeProfile>({
  // Basic Information
  size_sqft: 2000,
  age_years: 15,
  heating_type: '',
  insulation_type: '',
  window_type: '',
  num_floors: 2,
  num_occupants: 4,
  has_basement: false,
  has_attic: false,
  has_solar_panels: false,
  has_smart_thermostat: false,
  
  // Advanced - Location & Climate
  country: undefined,
  zip_code: undefined,
  climate_zone: undefined,
  
  // Advanced - Energy Details
  primary_energy_source: undefined,
  avg_monthly_energy_cost: undefined,
  avg_monthly_kwh: undefined,
  hvac_age_years: undefined,
  
  // Advanced - Building Characteristics
  roof_type: undefined,
  roof_age_years: undefined,
  
  // Advanced - Preferences
  budget_range: undefined,
  planning_to_sell_years: undefined,
});

const handleSubmit = () => {
  emit('submit', formData);
};
</script>

<style scoped>
h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

/* Enhanced Error Display */
.error-container {
  background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
  border: 2px solid #ef5350;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  box-shadow: 0 2px 8px rgba(239, 83, 80, 0.1);
}

.error-icon {
  font-size: 2rem;
  flex-shrink: 0;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.error-content {
  flex: 1;
}

.error-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: #c62828;
  margin-bottom: 0.5rem;
}

.error-message {
  color: #d32f2f;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.error-hint {
  color: #e57373;
  font-size: 0.9rem;
  font-style: italic;
}

.submit-btn {
  width: 100%;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #5c6bc0 0%, #3f51b5 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(63, 81, 181, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(63, 81, 181, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  h2 {
    font-size: 1.5rem;
  }
}
</style>
