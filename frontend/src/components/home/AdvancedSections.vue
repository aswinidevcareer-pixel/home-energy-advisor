<template>
  <div class="advanced-sections">
    <button
      type="button"
      class="toggle-button"
      @click="emit('toggle')"
    >
      <span class="toggle-icon">{{ showAdvanced ? '▼' : '▶' }}</span>
      <span class="toggle-text">
        {{ showAdvanced ? 'Hide' : 'Show' }} Advanced Options
      </span>
      <span class="toggle-hint">(optional - for more detailed analysis)</span>
    </button>

    <transition name="slide-fade">
      <div v-if="showAdvanced" class="advanced-content">
        <LocationSection 
          :model-value="modelValue" 
          @update:model-value="emit('update:modelValue', $event)"
        />
        <EnergyDetailsSection 
          :model-value="modelValue" 
          @update:model-value="emit('update:modelValue', $event)"
        />
        <BuildingSection 
          :model-value="modelValue" 
          @update:model-value="emit('update:modelValue', $event)"
        />
        <PreferencesSection 
          :model-value="modelValue" 
          @update:model-value="emit('update:modelValue', $event)"
        />
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import LocationSection from './LocationSection.vue';
import EnergyDetailsSection from './EnergyDetailsSection.vue';
import BuildingSection from './BuildingSection.vue';
import PreferencesSection from './PreferencesSection.vue';
import type { HomeProfile } from '../../types';

interface Props {
  modelValue: HomeProfile;
  showAdvanced: boolean;
}

defineProps<Props>();

const emit = defineEmits<{
  toggle: [];
  'update:modelValue': [value: HomeProfile];
}>();
</script>

<style scoped>
.advanced-sections {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.toggle-button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.toggle-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.toggle-button:active {
  transform: translateY(0);
}

.toggle-icon {
  font-size: 0.875rem;
  transition: transform 0.3s ease;
}

.toggle-text {
  flex-grow: 1;
  text-align: left;
}

.toggle-hint {
  font-size: 0.875rem;
  opacity: 0.9;
  font-weight: 400;
}

.advanced-content {
  margin-top: 1.5rem;
}

/* Transition animations */
.slide-fade-enter-active {
  transition: all 0.4s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(-20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
