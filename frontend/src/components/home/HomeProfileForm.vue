<template>
  <form @submit.prevent="handleSubmit">
    <h2>Tell us about your home</h2>
    
    <div class="form-grid">
      <div class="form-group">
        <label for="size">Home Size (sq ft)*</label>
        <input
          id="size"
          v-model.number="formData.size_sqft"
          type="number"
          min="100"
          max="50000"
          required
          placeholder="e.g., 2000"
        />
      </div>

      <div class="form-group">
        <label for="age">Home Age (years)*</label>
        <input
          id="age"
          v-model.number="formData.age_years"
          type="number"
          min="0"
          max="300"
          required
          placeholder="e.g., 15"
        />
      </div>

      <div class="form-group">
        <label for="heating">Heating Type*</label>
        <select id="heating" v-model="formData.heating_type" required>
          <option value="">Select...</option>
          <option value="gas">Gas</option>
          <option value="electric">Electric</option>
          <option value="oil">Oil</option>
          <option value="heat_pump">Heat Pump</option>
          <option value="solar">Solar</option>
          <option value="wood">Wood</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div class="form-group">
        <label for="insulation">Insulation Quality*</label>
        <select id="insulation" v-model="formData.insulation_type" required>
          <option value="">Select...</option>
          <option value="none">None</option>
          <option value="basic">Basic</option>
          <option value="moderate">Moderate</option>
          <option value="good">Good</option>
          <option value="excellent">Excellent</option>
        </select>
      </div>

      <div class="form-group">
        <label for="windows">Window Type*</label>
        <select id="windows" v-model="formData.window_type" required>
          <option value="">Select...</option>
          <option value="single_pane">Single Pane</option>
          <option value="double_pane">Double Pane</option>
          <option value="triple_pane">Triple Pane</option>
          <option value="low_e">Low-E</option>
        </select>
      </div>

      <div class="form-group">
        <label for="floors">Number of Floors*</label>
        <input
          id="floors"
          v-model.number="formData.num_floors"
          type="number"
          min="1"
          max="10"
          required
          placeholder="e.g., 2"
        />
      </div>

      <div class="form-group">
        <label for="occupants">Number of Occupants*</label>
        <input
          id="occupants"
          v-model.number="formData.num_occupants"
          type="number"
          min="1"
          max="20"
          required
          placeholder="e.g., 4"
        />
      </div>

      <div class="form-group">
        <label for="cost">Avg. Monthly Energy Cost (€)</label>
        <input
          id="cost"
          v-model.number="formData.avg_monthly_energy_cost"
          type="number"
          min="0"
          step="0.01"
          placeholder="e.g., 250.50"
        />
      </div>

      <div class="form-group">
        <label for="zip">Zip Code</label>
        <input
          id="zip"
          v-model="formData.zip_code"
          type="text"
          maxlength="10"
          placeholder="e.g., 94105"
        />
      </div>
    </div>

    <div class="form-grid">
      <div class="checkbox-group">
        <input
          id="basement"
          v-model="formData.has_basement"
          type="checkbox"
        />
        <label for="basement">Has Basement</label>
      </div>

      <div class="checkbox-group">
        <input
          id="attic"
          v-model="formData.has_attic"
          type="checkbox"
        />
        <label for="attic">Has Attic</label>
      </div>

      <div class="checkbox-group">
        <input
          id="solar"
          v-model="formData.has_solar_panels"
          type="checkbox"
        />
        <label for="solar">Has Solar Panels</label>
      </div>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <button type="submit" :disabled="loading">
      {{ loading ? 'Generating Recommendations...' : 'Get Energy Recommendations' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import type { HomeProfile } from '../types';

interface Props {
  loading: boolean;
  error: string;
}

interface Emits {
  (e: 'submit', formData: HomeProfile): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

const formData = reactive<HomeProfile>({
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
  avg_monthly_energy_cost: undefined,
  zip_code: ''
});

const handleSubmit = () => {
  emit('submit', formData);
};
</script>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #333;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #7986cb;
  box-shadow: 0 0 0 3px rgba(121, 134, 203, 0.15);
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-group input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.checkbox-group label {
  cursor: pointer;
  user-select: none;
  color: #555;
  font-weight: 500;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border-left: 4px solid #ef5350;
}

button {
  width: 100%;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #5c6bc0 0%, #3f51b5 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(63, 81, 181, 0.3);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
