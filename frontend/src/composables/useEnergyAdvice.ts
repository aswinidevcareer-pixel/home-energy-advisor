import { ref, type Ref } from 'vue';
import { homeApi, adviceApi } from '../services/api';
import type { HomeProfile, EnergyAdvice, Recommendation } from '../types';

// Priority order (high to low)
const priorityOrder: Record<string, number> = {
  'critical': 1,
  'high': 2,
  'medium': 3,
  'low': 4
};

// Difficulty order (easy to difficult)
const difficultyOrder: Record<string, number> = {
  'easy': 1,
  'moderate': 2,
  'difficult': 3
};

/**
 * Sort recommendations by priority, difficulty, and cost
 */
function sortRecommendations(recommendations: Recommendation[]): Recommendation[] {
  return [...recommendations].sort((a, b) => {
    // 1. Sort by priority (high to low)
    const priorityDiff = priorityOrder[a.priority.toLowerCase()] - priorityOrder[b.priority.toLowerCase()];
    if (priorityDiff !== 0) return priorityDiff;

    // 2. Sort by difficulty (easy to difficult)
    const diffA = a.implementation_difficulty?.toLowerCase() || 'moderate';
    const diffB = b.implementation_difficulty?.toLowerCase() || 'moderate';
    const difficultyDiff = (difficultyOrder[diffA] || 2) - (difficultyOrder[diffB] || 2);
    if (difficultyDiff !== 0) return difficultyDiff;

    // 3. Sort by cost (low to high)
    const costA = a.estimated_cost || 0;
    const costB = b.estimated_cost || 0;
    return costA - costB;
  });
}

export function useEnergyAdvice() {
  const loading: Ref<boolean> = ref(false);
  const error: Ref<string | null> = ref(null);
  const advice: Ref<EnergyAdvice | null> = ref(null);

  /**
   * Submit home profile and generate energy advice
   */
  const generateAdvice = async (profile: HomeProfile): Promise<void> => {
    loading.value = true;
    error.value = null;
    advice.value = null;

    try {
      // Step 1: Create home profile
      const homeResponse = await homeApi.createHome(profile);
      
      // Step 2: Generate advice
      const adviceResponse = await adviceApi.getAdvice(homeResponse.id);
      
      // Step 3: Sort recommendations
      adviceResponse.recommendations = sortRecommendations(adviceResponse.recommendations);
      
      advice.value = adviceResponse;
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'An unexpected error occurred';
      console.error('Error generating advice:', err);
    } finally {
      loading.value = false;
    }
  };

  /**
   * Reset the advice state
   */
  const reset = () => {
    loading.value = false;
    error.value = null;
    advice.value = null;
  };

  return {
    loading,
    error,
    advice,
    generateAdvice,
    reset
  };
}
