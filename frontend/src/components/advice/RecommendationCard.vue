<template>
  <div class="recommendation-card">
    <div class="recommendation-header">
      <div>
        <div class="recommendation-title">{{ recommendation.title }}</div>
        <span class="category-badge">{{ formattedCategory }}</span>
      </div>
      <span :class="`priority-badge priority-${recommendation.priority}`">
        {{ recommendation.priority }}
      </span>
    </div>

    <p class="recommendation-description">{{ recommendation.description }}</p>

    <div class="recommendation-metrics">
      <div v-if="recommendation.estimated_savings_annual" class="metric">
        <span class="metric-label">Annual Savings</span>
        <span class="metric-value">€{{ recommendation.estimated_savings_annual.toFixed(2) }}</span>
      </div>

      <div v-if="recommendation.estimated_cost" class="metric">
        <span class="metric-label">Implementation Cost</span>
        <span class="metric-value">€{{ recommendation.estimated_cost.toFixed(2) }}</span>
      </div>

      <div v-if="recommendation.payback_period_years" class="metric">
        <span class="metric-label">Payback Period</span>
        <span class="metric-value">{{ recommendation.payback_period_years.toFixed(1) }} years</span>
      </div>

      <div v-if="recommendation.implementation_difficulty" class="metric">
        <span class="metric-label">Difficulty</span>
        <span class="difficulty-badge">{{ recommendation.implementation_difficulty }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Recommendation } from '../types';

interface Props {
  recommendation: Recommendation;
}

const props = defineProps<Props>();

const formattedCategory = computed(() => {
  return props.recommendation.category
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
});
</script>

<style scoped>
.recommendation-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.recommendation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.recommendation-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #37474f;
  margin-bottom: 0.5rem;
}

.category-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #e3f2fd;
  color: #1565c0;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.priority-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
}

.priority-critical {
  background: #ffebee;
  color: #d32f2f;
}

.priority-high {
  background: #fff3e0;
  color: #f57c00;
}

.priority-medium {
  background: #fff9c4;
  color: #f9a825;
}

.priority-low {
  background: #e8f5e9;
  color: #388e3c;
}

.recommendation-description {
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.recommendation-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-label {
  font-size: 0.85rem;
  color: #888;
  font-weight: 500;
}

.metric-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #5c6bc0;
}

.difficulty-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f5f5f5;
  color: #546e7a;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
