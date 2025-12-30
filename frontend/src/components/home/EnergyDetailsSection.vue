<template>
  <section class="form-section">
    <h3>⚡ Energy Details</h3>
    <div class="form-grid">
      <FormField
        id="energy_source"
        :model-value="modelValue.primary_energy_source"
        @update:model-value="updateField('primary_energy_source', $event)"
        label="Primary Energy Source"
        type="select"
        :options="energySourceOptions"
      />

      <FormField
        id="cost"
        :model-value="modelValue.avg_monthly_energy_cost"
        @update:model-value="updateField('avg_monthly_energy_cost', $event)"
        label="Avg. Monthly Energy Cost (€)"
        type="number"
        :min="0"
        step="0.01"
        placeholder="e.g., 250.50"
      />

      <FormField
        id="kwh"
        :model-value="modelValue.avg_monthly_kwh"
        @update:model-value="updateField('avg_monthly_kwh', $event)"
        label="Avg. Monthly kWh Usage"
        type="number"
        :min="0"
        step="1"
        placeholder="e.g., 900"
      />

      <FormField
        id="hvac_age"
        :model-value="modelValue.hvac_age_years"
        @update:model-value="updateField('hvac_age_years', $event)"
        label="HVAC System Age (years)"
        type="number"
        :min="0"
        :max="50"
        placeholder="e.g., 8"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import FormField from '../common/FormField.vue';
import type { HomeProfile } from '../../types';

interface Props {
  modelValue: HomeProfile;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'update:modelValue': [value: HomeProfile];
}>();

const updateField = (field: keyof HomeProfile, value: any) => {
  // Mutate the original object to maintain reactivity
  (props.modelValue as any)[field] = value;
};

const energySourceOptions = [
  { value: '', label: 'Select...' },
  { value: 'electricity', label: 'Electricity' },
  { value: 'natural_gas', label: 'Natural Gas' },
  { value: 'propane', label: 'Propane' },
  { value: 'oil', label: 'Heating Oil' },
  { value: 'mixed', label: 'Mixed Sources' }
];
</script>

<style scoped>
.form-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #5c6bc0;
}

.form-section h3 {
  color: #3f51b5;
  margin: 0 0 1.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
</style>
