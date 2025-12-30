from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class HeatingType(str, Enum):
    GAS = "gas"
    ELECTRIC = "electric"
    OIL = "oil"
    HEAT_PUMP = "heat_pump"
    SOLAR = "solar"
    WOOD = "wood"
    OTHER = "other"


class InsulationType(str, Enum):
    NONE = "none"
    BASIC = "basic"
    MODERATE = "moderate"
    GOOD = "good"
    EXCELLENT = "excellent"


class WindowType(str, Enum):
    SINGLE_PANE = "single_pane"
    DOUBLE_PANE = "double_pane"
    TRIPLE_PANE = "triple_pane"
    LOW_E = "low_e"


class ClimateZone(str, Enum):
    HOT_HUMID = "hot_humid"
    HOT_DRY = "hot_dry"
    MIXED_HUMID = "mixed_humid"
    MIXED_DRY = "mixed_dry"
    COLD = "cold"
    VERY_COLD = "very_cold"
    SUBARCTIC = "subarctic"
    MARINE = "marine"


class EnergySource(str, Enum):
    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    PROPANE = "propane"
    OIL = "oil"
    MIXED = "mixed"


class RoofType(str, Enum):
    ASPHALT_SHINGLE = "asphalt_shingle"
    METAL = "metal"
    TILE = "tile"
    SLATE = "slate"
    FLAT = "flat"
    WOOD_SHAKE = "wood_shake"


class BudgetRange(str, Enum):
    LOW = "low"           # Under $2,000
    MEDIUM = "medium"     # $2,000 - $10,000
    HIGH = "high"         # $10,000 - $30,000
    PREMIUM = "premium"   # Over $30,000


class HomeProfile(BaseModel):
    id: Optional[str] = None
    # Basic Information
    size_sqft: int = Field(gt=0, le=50000, description="Home size in square feet")
    age_years: int = Field(ge=0, le=300, description="Age of the home in years")
    heating_type: HeatingType
    insulation_type: InsulationType
    window_type: WindowType
    num_floors: int = Field(ge=1, le=10, description="Number of floors")
    num_occupants: int = Field(ge=1, le=20, description="Number of occupants")
    has_basement: bool = Field(default=False)
    has_attic: bool = Field(default=False)
    has_solar_panels: bool = Field(default=False)
    has_smart_thermostat: bool = Field(default=False)
    
    # Advanced - Location & Climate
    country: Optional[str] = Field(default=None, max_length=100, description="Country")
    zip_code: Optional[str] = Field(default=None, max_length=10, description="Zip code for climate considerations")
    climate_zone: Optional[ClimateZone] = Field(default=None, description="Climate zone classification")
    
    # Advanced - Energy Details
    primary_energy_source: Optional[EnergySource] = Field(default=None, description="Primary energy source")
    avg_monthly_energy_cost: Optional[float] = Field(default=None, ge=0, description="Average monthly energy cost in USD")
    avg_monthly_kwh: Optional[float] = Field(default=None, ge=0, description="Average monthly electricity consumption in kWh")
    hvac_age_years: Optional[int] = Field(default=None, ge=0, le=50, description="Age of HVAC system")
    
    # Advanced - Building Characteristics
    roof_type: Optional[RoofType] = Field(default=None, description="Type of roof")
    roof_age_years: Optional[int] = Field(default=None, ge=0, le=100, description="Age of roof")
    
    # Advanced - Preferences
    budget_range: Optional[BudgetRange] = Field(default=None, description="Budget range for improvements")
    planning_to_sell_years: Optional[int] = Field(default=None, ge=0, le=50, description="Planning to sell within this many years")
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.replace('-', '').isdigit():
            raise ValueError('Zip code must contain only digits and hyphens')
        return v

    def __str__(self) -> str:
        """String representation suitable for LLM prompts and logging."""
        details = f"""Home Profile:
- Size: {self.size_sqft} square feet
- Age: {self.age_years} years old
- Heating Type: {self.heating_type}
- Insulation: {self.insulation_type}
- Windows: {self.window_type}
- Floors: {self.num_floors}
- Occupants: {self.num_occupants}
- Basement: {"Yes" if self.has_basement else "No"}
- Attic: {"Yes" if self.has_attic else "No"}
- Solar Panels: {"Yes" if self.has_solar_panels else "No"}
- Smart Thermostat: {"Yes" if self.has_smart_thermostat else "No"}"""
        
        # Location & Climate
        if self.country:
            details += f"\n- Country: {self.country}"
        if self.zip_code:
            details += f"\n- Zip Code: {self.zip_code}"
        if self.climate_zone:
            details += f"\n- Climate Zone: {self.climate_zone}"
        
        # Energy Details
        if self.primary_energy_source:
            details += f"\n- Primary Energy Source: {self.primary_energy_source}"
        if self.avg_monthly_energy_cost:
            details += f"\n- Average Monthly Energy Cost: ${self.avg_monthly_energy_cost:.2f}"
        if self.avg_monthly_kwh:
            details += f"\n- Average Monthly Electricity Usage: {self.avg_monthly_kwh:.1f} kWh"
        if self.hvac_age_years is not None:
            details += f"\n- HVAC System Age: {self.hvac_age_years} years"
        
        # Building Characteristics
        if self.roof_type:
            details += f"\n- Roof Type: {self.roof_type}"
        if self.roof_age_years is not None:
            details += f"\n- Roof Age: {self.roof_age_years} years"
        
        # Preferences
        if self.budget_range:
            details += f"\n- Budget Range: {self.budget_range}"
        if self.planning_to_sell_years is not None:
            details += f"\n- Planning to Sell Within: {self.planning_to_sell_years} years"
        
        return details

    class Config:
        use_enum_values = True
