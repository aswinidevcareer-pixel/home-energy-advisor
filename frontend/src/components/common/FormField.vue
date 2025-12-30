<template>
  <div class="form-group">
    <label :for="id">{{ label }}</label>
    <input
      v-if="type !== 'select'"
      :id="id"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', parseValue($event))"
      :min="min"
      :max="max"
      :step="step"
      :maxlength="maxlength"
      :required="required"
      :placeholder="placeholder"
    />
    <select
      v-else
      :id="id"
      :value="modelValue"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      :required="required"
    >
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: string;
  modelValue: any;
  label: string;
  type?: 'text' | 'number' | 'select';
  min?: number;
  max?: number;
  step?: number | string;
  maxlength?: number;
  required?: boolean;
  placeholder?: string;
  options?: Array<{ value: string | number; label: string }>;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  required: false
});

defineEmits<{
  (e: 'update:modelValue', value: any): void;
}>();

const parseValue = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = target.value;
  
  if (props.type === 'number') {
    // Return undefined for empty strings to allow proper validation
    return value === '' ? undefined : Number(value);
  }
  
  return value;
};
</script>

<style scoped>
.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
  font-size: 0.95rem;
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
</style>
