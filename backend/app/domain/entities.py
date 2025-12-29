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


class HomeProfile(BaseModel):
    id: Optional[str] = None
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
    avg_monthly_energy_cost: Optional[float] = Field(default=None, ge=0, description="Average monthly energy cost in EUR")
    zip_code: Optional[str] = Field(default=None, max_length=10, description="Zip code for climate considerations")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.replace('-', '').isdigit():
            raise ValueError('Zip code must contain only digits and hyphens')
        return v

    class Config:
        use_enum_values = True
