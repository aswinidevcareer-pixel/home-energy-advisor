<template>
  <section class="form-section">
    <h3>📍 Location & Climate</h3>
    <div class="form-grid">
      <FormField
        id="country"
        :model-value="modelValue.country"
        @update:model-value="updateField('country', $event)"
        label="Country"
        type="text"
        :maxlength="100"
        placeholder="e.g., Germany"
      />

      <FormField
        id="zip"
        :model-value="modelValue.zip_code"
        @update:model-value="updateField('zip_code', $event)"
        label="Zip Code"
        type="text"
        :maxlength="10"
        placeholder="e.g., 94105"
      />

      <FormField
        id="climate"
        :model-value="modelValue.climate_zone"
        @update:model-value="updateField('climate_zone', $event)"
        label="Climate Zone"
        type="select"
        :options="climateOptions"
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

const climateOptions = [
  { value: '', label: 'Select...' },
  { value: 'hot_humid', label: 'Hot-Humid' },
  { value: 'hot_dry', label: 'Hot-Dry (Desert)' },
  { value: 'mixed_humid', label: 'Mixed-Humid' },
  { value: 'mixed_dry', label: 'Mixed-Dry' },
  { value: 'cold', label: 'Cold' },
  { value: 'very_cold', label: 'Very Cold' },
  { value: 'subarctic', label: 'Subarctic' },
  { value: 'marine', label: 'Marine (Coastal)' }
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
