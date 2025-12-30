export interface HomeProfile {
  // Basic Information
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
  has_smart_thermostat: boolean;
  
  // Advanced - Location & Climate
  country?: string;
  zip_code?: string;
  climate_zone?: string;
  
  // Advanced - Energy Details
  primary_energy_source?: string;
  avg_monthly_energy_cost?: number;
  avg_monthly_kwh?: number;
  hvac_age_years?: number;
  
  // Advanced - Building Characteristics
  roof_type?: string;
  roof_age_years?: number;
  
  // Advanced - Preferences
  budget_range?: string;
  planning_to_sell_years?: number;
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
