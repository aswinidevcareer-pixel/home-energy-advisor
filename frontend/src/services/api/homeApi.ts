import { apiClient } from './client';
import type { HomeProfile, HomeResponse } from '../../types';

export const homeApi = {
  /**
   * Create a new home profile
   */
  createHome: async (profile: HomeProfile): Promise<HomeResponse> => {
    const response = await apiClient.post<HomeResponse>('/homes', profile);
    return response.data;
  },

  /**
   * Get a home profile by ID
   */
  getHome: async (id: string): Promise<HomeResponse> => {
    const response = await apiClient.get<HomeResponse>(`/homes/${id}`);
    return response.data;
  }
};
