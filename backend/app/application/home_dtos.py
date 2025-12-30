from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.domain.entities import (
    HeatingType, 
    InsulationType, 
    WindowType,
    ClimateZone,
    EnergySource,
    RoofType,
    BudgetRange
)


class CreateHomeRequest(BaseModel):
    # Basic Information
    size_sqft: int = Field(gt=0, le=50000, description="Home size in square feet", examples=[2000])
    age_years: int = Field(ge=0, le=300, description="Age of the home in years", examples=[15])
    heating_type: HeatingType = Field(description="Type of heating system", examples=["gas"])
    insulation_type: InsulationType = Field(description="Quality of insulation", examples=["moderate"])
    window_type: WindowType = Field(description="Type of windows", examples=["double_pane"])
    num_floors: int = Field(ge=1, le=10, description="Number of floors", examples=[2])
    num_occupants: int = Field(ge=1, le=20, description="Number of occupants", examples=[4])
    has_basement: bool = Field(default=False, description="Whether the home has a basement")
    has_attic: bool = Field(default=False, description="Whether the home has an attic")
    has_solar_panels: bool = Field(default=False, description="Whether the home has solar panels")
    has_smart_thermostat: bool = Field(default=False, description="Whether the home has a smart thermostat")
    
    # Advanced - Location & Climate
    country: Optional[str] = Field(default=None, max_length=100, description="Country", examples=["United States"])
    zip_code: Optional[str] = Field(default=None, max_length=10, description="Zip code for climate considerations", examples=["94105"])
    climate_zone: Optional[ClimateZone] = Field(default=None, description="Climate zone classification", examples=["cold"])
    
    # Advanced - Energy Details
    primary_energy_source: Optional[EnergySource] = Field(default=None, description="Primary energy source", examples=["natural_gas"])
    avg_monthly_energy_cost: Optional[float] = Field(default=None, ge=0, description="Average monthly energy cost in USD", examples=[250.50])
    avg_monthly_kwh: Optional[float] = Field(default=None, ge=0, description="Average monthly electricity consumption in kWh", examples=[900.0])
    hvac_age_years: Optional[int] = Field(default=None, ge=0, le=50, description="Age of HVAC system", examples=[8])
    
    # Advanced - Building Characteristics
    roof_type: Optional[RoofType] = Field(default=None, description="Type of roof", examples=["asphalt_shingle"])
    roof_age_years: Optional[int] = Field(default=None, ge=0, le=100, description="Age of roof", examples=[10])
    
    # Advanced - Preferences
    budget_range: Optional[BudgetRange] = Field(default=None, description="Budget range for improvements", examples=["medium"])
    planning_to_sell_years: Optional[int] = Field(default=None, ge=0, le=50, description="Planning to sell within this many years", examples=[5])

    class Config:
        json_schema_extra = {
            "example": {
                "size_sqft": 2000,
                "age_years": 15,
                "heating_type": "gas",
                "insulation_type": "moderate",
                "window_type": "double_pane",
                "num_floors": 2,
                "num_occupants": 4,
                "has_basement": True,
                "has_attic": True,
                "has_solar_panels": False,
                "has_smart_thermostat": False,
                "country": "United States",
                "zip_code": "94105",
                "climate_zone": "cold",
                "primary_energy_source": "natural_gas",
                "avg_monthly_energy_cost": 250.50,
                "avg_monthly_kwh": 900.0,
                "hvac_age_years": 8,
                "roof_type": "asphalt_shingle",
                "roof_age_years": 10,
                "budget_range": "medium",
                "planning_to_sell_years": 5
            }
        }


class HomeResponse(BaseModel):
    id: str
    # Basic Information
    size_sqft: int
    age_years: int
    heating_type: str
    insulation_type: str
    window_type: str
    num_floors: int
    num_occupants: int
    has_basement: bool
    has_attic: bool
    has_solar_panels: bool
    has_smart_thermostat: bool
    
    # Advanced - Location & Climate
    country: Optional[str]
    zip_code: Optional[str]
    climate_zone: Optional[str]
    
    # Advanced - Energy Details
    primary_energy_source: Optional[str]
    avg_monthly_energy_cost: Optional[float]
    avg_monthly_kwh: Optional[float]
    hvac_age_years: Optional[int]
    
    # Advanced - Building Characteristics
    roof_type: Optional[str]
    roof_age_years: Optional[int]
    
    # Advanced - Preferences
    budget_range: Optional[str]
    planning_to_sell_years: Optional[int]
    
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "size_sqft": 2000,
                "age_years": 15,
                "heating_type": "gas",
                "insulation_type": "moderate",
                "window_type": "double_pane",
                "num_floors": 2,
                "num_occupants": 4,
                "has_basement": True,
                "has_attic": True,
                "has_solar_panels": False,
                "has_smart_thermostat": False,
                "country": "United States",
                "zip_code": "94105",
                "climate_zone": "cold",
                "primary_energy_source": "natural_gas",
                "avg_monthly_energy_cost": 250.50,
                "avg_monthly_kwh": 900.0,
                "hvac_age_years": 8,
                "roof_type": "asphalt_shingle",
                "roof_age_years": 10,
                "budget_range": "medium",
                "planning_to_sell_years": 5,
                "created_at": "2025-12-30T10:30:00Z",
                "updated_at": "2025-12-30T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "size_sqft must be greater than 0"
            }
        }
