<template>
  <section class="form-section">
    <h3>🏠 Building Details</h3>
    <div class="form-grid">
      <FormField
        id="roof_type"
        :model-value="modelValue.roof_type"
        @update:model-value="updateField('roof_type', $event)"
        label="Roof Type"
        type="select"
        :options="roofTypeOptions"
      />

      <FormField
        id="roof_age"
        :model-value="modelValue.roof_age_years"
        @update:model-value="updateField('roof_age_years', $event)"
        label="Roof Age (years)"
        type="number"
        :min="0"
        :max="100"
        placeholder="e.g., 12"
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

const roofTypeOptions = [
  { value: '', label: 'Select...' },
  { value: 'asphalt_shingle', label: 'Asphalt Shingle' },
  { value: 'metal', label: 'Metal' },
  { value: 'tile', label: 'Tile' },
  { value: 'slate', label: 'Slate' },
  { value: 'flat', label: 'Flat' },
  { value: 'other', label: 'Other' }
];
</script>

<style scoped>
.form-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #66bb6a;
}

.form-section h3 {
  color: #43a047;
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
