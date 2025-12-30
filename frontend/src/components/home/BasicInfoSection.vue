<template>
  <section class="form-section">
    <h3>🏠 Basic Information</h3>
    <div class="form-grid">
      <FormField
        id="size"
        :model-value="modelValue.size_sqft"
        @update:model-value="updateField('size_sqft', $event)"
        label="Home Size (sq ft)*"
        type="number"
        :min="100"
        :max="50000"
        required
        placeholder="e.g., 2000"
      />

      <FormField
        id="age"
        :model-value="modelValue.age_years"
        @update:model-value="updateField('age_years', $event)"
        label="Home Age (years)*"
        type="number"
        :min="0"
        :max="300"
        required
        placeholder="e.g., 15"
      />

      <FormField
        id="heating"
        :model-value="modelValue.heating_type"
        @update:model-value="updateField('heating_type', $event)"
        label="Heating Type*"
        type="select"
        required
        :options="heatingOptions"
      />

      <FormField
        id="insulation"
        :model-value="modelValue.insulation_type"
        @update:model-value="updateField('insulation_type', $event)"
        label="Insulation Quality*"
        type="select"
        required
        :options="insulationOptions"
      />

      <FormField
        id="windows"
        :model-value="modelValue.window_type"
        @update:model-value="updateField('window_type', $event)"
        label="Window Type*"
        type="select"
        required
        :options="windowOptions"
      />

      <FormField
        id="floors"
        :model-value="modelValue.num_floors"
        @update:model-value="updateField('num_floors', $event)"
        label="Number of Floors*"
        type="number"
        :min="1"
        :max="10"
        required
        placeholder="e.g., 2"
      />

      <FormField
        id="occupants"
        :model-value="modelValue.num_occupants"
        @update:model-value="updateField('num_occupants', $event)"
        label="Number of Occupants*"
        type="number"
        :min="1"
        :max="20"
        required
        placeholder="e.g., 4"
      />
    </div>

    <div class="form-grid checkbox-grid">
      <CheckboxField
        id="basement"
        :model-value="modelValue.has_basement"
        @update:model-value="updateField('has_basement', $event)"
        label="Has Basement"
      />

      <CheckboxField
        id="attic"
        :model-value="modelValue.has_attic"
        @update:model-value="updateField('has_attic', $event)"
        label="Has Attic"
      />

      <CheckboxField
        id="smart_thermostat"
        :model-value="modelValue.has_smart_thermostat"
        @update:model-value="updateField('has_smart_thermostat', $event)"
        label="Has Smart Thermostat"
      />

      <CheckboxField
        id="solar"
        :model-value="modelValue.has_solar_panels"
        @update:model-value="updateField('has_solar_panels', $event)"
        label="Has Solar Panels"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import FormField from '../common/FormField.vue';
import CheckboxField from '../common/CheckboxField.vue';
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

const heatingOptions = [
  { value: '', label: 'Select...' },
  { value: 'gas', label: 'Gas' },
  { value: 'electric', label: 'Electric' },
  { value: 'oil', label: 'Oil' },
  { value: 'heat_pump', label: 'Heat Pump' },
  { value: 'solar', label: 'Solar' },
  { value: 'wood', label: 'Wood' },
  { value: 'other', label: 'Other' }
];

const insulationOptions = [
  { value: '', label: 'Select...' },
  { value: 'none', label: 'None' },
  { value: 'basic', label: 'Basic' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'good', label: 'Good' },
  { value: 'excellent', label: 'Excellent' }
];

const windowOptions = [
  { value: '', label: 'Select...' },
  { value: 'single_pane', label: 'Single Pane' },
  { value: 'double_pane', label: 'Double Pane' },
  { value: 'triple_pane', label: 'Triple Pane' },
  { value: 'low_e', label: 'Low-E' }
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

.checkbox-grid {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  margin-top: 1rem;
}
</style>
