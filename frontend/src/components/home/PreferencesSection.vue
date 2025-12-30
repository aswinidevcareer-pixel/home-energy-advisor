<template>
  <section class="form-section">
    <h3>💰 Budget & Planning</h3>
    <div class="form-grid">
      <FormField
        id="budget_range"
        :model-value="modelValue.budget_range"
        @update:model-value="updateField('budget_range', $event)"
        label="Budget Range for Improvements"
        type="select"
        :options="budgetOptions"
      />

      <FormField
        id="planning_to_sell"
        :model-value="modelValue.planning_to_sell_years"
        @update:model-value="updateField('planning_to_sell_years', $event)"
        label="Planning to Sell Within (years)"
        type="number"
        :min="0"
        :max="50"
        placeholder="e.g., 5"
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

const budgetOptions = [
  { value: '', label: 'Select...' },
  { value: 'low', label: 'Low (<$5,000)' },
  { value: 'medium', label: 'Medium ($5,000-$15,000)' },
  { value: 'high', label: 'High ($15,000-$50,000)' },
  { value: 'premium', label: 'Premium (>$50,000)' }
];
</script>

<style scoped>
.form-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #ffa726;
}

.form-section h3 {
  color: #f57c00;
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
