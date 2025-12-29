export interface HomeProfile {
  size_sqft: number;
  age_years: number;
  heating_type: string;
  insulation_type: string;
  window_type: string;
  num_floors: number;
  num_occupants: number;
  has_basement: boolean;
  has_attic: boolean;
  has_solar_panels: boolean;
  avg_monthly_energy_cost?: number;
  zip_code?: string;
}

export interface HomeResponse extends HomeProfile {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface Recommendation {
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  category: string;
  estimated_savings_annual?: number;
  estimated_cost?: number;
  payback_period_years?: number;
  implementation_difficulty?: string;
}

export interface EnergyAdvice {
  home_id: string;
  recommendations: Recommendation[];
  summary: string;
  estimated_total_annual_savings?: number;
  generated_at: string;
  llm_provider: string;
}
