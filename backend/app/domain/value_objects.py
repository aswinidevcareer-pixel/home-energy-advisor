from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationCategory(str, Enum):
    INSULATION = "insulation"
    HEATING_COOLING = "heating_cooling"
    WINDOWS = "windows"
    APPLIANCES = "appliances"
    RENEWABLE_ENERGY = "renewable_energy"
    BEHAVIORAL = "behavioral"
    OTHER = "other"


class ImplementationDifficulty(str, Enum):
    EASY = "easy"
    MODERATE = "moderate"
    Difficult = "difficult"

class Recommendation(BaseModel):
    title: str = Field(description="Brief title of the recommendation")
    description: str = Field(description="Detailed description")
    priority: Priority
    category: RecommendationCategory
    estimated_savings_annual: float | None = Field(
        default=None, 
        gt=0,
        description="Estimated annual savings in EUR; must be > 0 EUR. Calculated as estimated_cost / payback_period_years"
    )
    estimated_cost: float | None = Field(
        default=None, 
        gt=0,
        description="Estimated implementation cost in EUR; must be = 0 EUR"
    )
    payback_period_years: float | None = Field(
        default=None, 
        gt=0,
        description="Estimated payback period in years; must be > 0"
    )
    implementation_difficulty: ImplementationDifficulty = Field(
        default=ImplementationDifficulty.MODERATE, 
        description="Difficulty level of the implementation"
    )


class EnergyAdvice(BaseModel):
    home_id: str
    recommendations: List[Recommendation]
    summary: str = Field(description="Overall summary of energy efficiency status")
    estimated_total_annual_savings: float | None = Field(
        default=None,
        gt=0,
        description="Total estimated annual savings in EUR if all recommendations are implemented; must be >= 1 EUR. Sum of all estimated_savings_annual values from recommendations"
    )
    generated_at: datetime
    llm_provider: str = Field(description="LLM provider used to generate advice")