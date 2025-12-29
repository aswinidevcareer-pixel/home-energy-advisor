from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.domain.value_objects import Priority, RecommendationCategory


class RecommendationResponse(BaseModel):
    title: str = Field(description="Brief title of the recommendation")
    description: str = Field(description="Detailed explanation of the recommendation and its benefits")
    priority: Priority = Field(description="Priority level: critical, high, medium, or low")
    category: RecommendationCategory = Field(description="Category of energy improvement")
    estimated_savings_annual: Optional[float] = Field(
        default=None,
        description="Estimated annual savings in EUR"
    )
    estimated_cost: Optional[float] = Field(
        default=None,
        description="Estimated implementation cost in EUR"
    )
    payback_period_years: Optional[float] = Field(
        default=None,
        description="Estimated payback period in years (cost / annual savings)"
    )
    implementation_difficulty: Optional[str] = Field(
        default=None,
        description="Difficulty level: Easy, Moderate, or Difficult"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Upgrade to LED Lighting",
                "description": "Replace all incandescent and CFL bulbs with LED bulbs throughout the home. LEDs use 75% less energy and last 25 times longer.",
                "priority": "medium",
                "category": "appliances",
                "estimated_savings_annual": 150.0,
                "estimated_cost": 200.0,
                "payback_period_years": 1.3,
                "implementation_difficulty": "Easy"
            }
        }


class EnergyAdviceResponse(BaseModel):
    home_id: str = Field(description="Unique identifier of the home profile")
    recommendations: List[RecommendationResponse] = Field(description="List of energy efficiency recommendations")
    summary: str = Field(description="Overall summary of the home's energy efficiency status and improvement potential")
    estimated_total_annual_savings: Optional[float] = Field(
        default=None,
        description="Total estimated annual savings in EUR if all recommendations are implemented"
    )
    generated_at: datetime = Field(description="Timestamp when the advice was generated")
    llm_provider: str = Field(description="Name of the LLM provider used to generate the recommendations")

    class Config:
        json_schema_extra = {
            "example": {
                "home_id": "123e4567-e89b-12d3-a456-426614174000",
                "summary": "Your 15-year-old home has moderate energy efficiency with significant potential for improvement, particularly in insulation and heating system optimization.",
                "recommendations": [
                    {
                        "title": "Upgrade Attic Insulation",
                        "description": "Increase attic insulation to R-49. Your moderate insulation is likely inadequate for optimal efficiency.",
                        "priority": "high",
                        "category": "insulation",
                        "estimated_savings_annual": 500.0,
                        "estimated_cost": 2000.0,
                        "payback_period_years": 4.0,
                        "implementation_difficulty": "Moderate"
                    }
                ],
                "estimated_total_annual_savings": 2500.0,
                "generated_at": "2025-12-21T10:30:00Z",
                "llm_provider": "ollama-llama3.2"
            }
        }


class LLMProviderInfo(BaseModel):
    provider_type: str = Field(description="Type of LLM provider (e.g., 'ollama', 'openai', 'anthropic')")
    provider_name: str = Field(description="Full provider name including model (e.g., 'ollama-llama3.2')")
    is_available: bool = Field(description="Whether the LLM provider is currently available and responding")
    
    class Config:
        json_schema_extra = {
            "example": {
                "provider_type": "ollama",
                "provider_name": "ollama-llama3.2",
                "is_available": True
            }
        }
