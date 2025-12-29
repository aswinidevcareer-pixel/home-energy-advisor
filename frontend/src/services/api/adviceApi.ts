import { apiClient } from './client';
import type { EnergyAdvice } from '../../types';

export const adviceApi = {
  /**
   * Generate energy-saving advice for a home
   */
  getAdvice: async (homeId: string): Promise<EnergyAdvice> => {
    const response = await apiClient.post<EnergyAdvice>(`/homes/${homeId}/advice`);
    return response.data;
  }
};
