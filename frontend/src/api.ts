import axios from 'axios';
import type { HomeProfile, HomeResponse, EnergyAdvice } from './types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const homeApi = {
  createHome: async (profile: HomeProfile): Promise<HomeResponse> => {
    const response = await api.post<HomeResponse>('/homes', profile);
    return response.data;
  },

  getHome: async (id: string): Promise<HomeResponse> => {
    const response = await api.get<HomeResponse>(`/homes/${id}`);
    return response.data;
  },

  getAdvice: async (homeId: string): Promise<EnergyAdvice> => {
    const response = await api.post<EnergyAdvice>(`/homes/${homeId}/advice`);
    return response.data;
  }
};
