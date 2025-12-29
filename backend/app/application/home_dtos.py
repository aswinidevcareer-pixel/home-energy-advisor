from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.domain.entities import HeatingType, InsulationType, WindowType


class CreateHomeRequest(BaseModel):
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
    avg_monthly_energy_cost: Optional[float] = Field(default=None, ge=0, description="Average monthly energy cost in EUR", examples=[250.50])
    zip_code: Optional[str] = Field(default=None, max_length=10, description="Zip code for climate considerations", examples=["94105"])

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
                "avg_monthly_energy_cost": 250.50,
                "zip_code": "94105"
            }
        }


class HomeResponse(BaseModel):
    id: str
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
    avg_monthly_energy_cost: Optional[float]
    zip_code: Optional[str]
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
                "avg_monthly_energy_cost": 250.50,
                "zip_code": "94105",
                "created_at": "2025-12-21T10:30:00Z",
                "updated_at": "2025-12-21T10:30:00Z"
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
