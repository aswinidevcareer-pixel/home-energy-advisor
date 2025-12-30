<template>
  <div class="checkbox-group">
    <input
      :id="id"
      type="checkbox"
      :checked="modelValue"
      @change="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
    />
    <label :for="id">{{ label }}</label>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: string;
  modelValue: boolean;
  label: string;
}

defineProps<Props>();

defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();
</script>

<style scoped>
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-group input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #5c6bc0;
}

.checkbox-group label {
  cursor: pointer;
  user-select: none;
  color: #555;
  font-weight: 500;
}
</style>
