import json
from datetime import datetime
from typing import Optional
from app.domain.entities import HomeProfile
from app.domain.value_objects import EnergyAdvice, Recommendation
from app.domain.repositories import HomeRepository
from app.infrastructure.llm.base import LLMProvider
from app.application.prompt_builder import EnergyAdvicePromptBuilder
from app.infrastructure.llm.exceptions import LLMValidationError


class EnergyAdviceService:
    def __init__(
        self,
        home_repository: HomeRepository,
        llm_provider: LLMProvider
    ):
        self.home_repository = home_repository
        self.llm_provider = llm_provider
        self.prompt_builder = EnergyAdvicePromptBuilder()

    async def generate_advice(self, home_id: str) -> EnergyAdvice:
        home = await self.home_repository.get_by_id(home_id)
        
        if not home:
            raise ValueError(f"Home with id '{home_id}' not found")

        prompt = self.prompt_builder.build_prompt(home)
        
        llm_response = await self.llm_provider.generate_completion(
            prompt=prompt,
            temperature=0.7,
            response_format=EnergyAdvice.model_json_schema(),
            max_tokens=4000
        )
        
        advice_data = self._parse_llm_response(llm_response)
        
        # Process recommendations and calculate missing fields
        recommendations = []
        for rec_data in advice_data.get("recommendations", []):
            # Convert 0 or negative values to None for fields with gt=0 validation
            for field in ["estimated_savings_annual", "estimated_cost", "payback_period_years"]:
                if rec_data.get(field) is not None and rec_data.get(field) <= 0:
                    rec_data[field] = None
            
            # Calculate estimated_savings_annual if not provided
            if rec_data.get("estimated_savings_annual") is None:
                estimated_cost = rec_data.get("estimated_cost")
                payback_period = rec_data.get("payback_period_years")
                
                if estimated_cost is not None and payback_period is not None and payback_period > 0:
                    rec_data["estimated_savings_annual"] = estimated_cost / payback_period
                # Otherwise leave as None (optional field)
            
            recommendations.append(Recommendation(**rec_data))
        
        # Calculate total annual savings if not provided by LLM
        estimated_total_annual_savings = advice_data.get("estimated_total_annual_savings")
        if estimated_total_annual_savings is None:
            # Sum up all individual recommendation savings
            total_savings = sum(
                rec.estimated_savings_annual 
                for rec in recommendations 
                if rec.estimated_savings_annual is not None
            )
            # Use the calculated total if available, otherwise leave as None (optional field)
            estimated_total_annual_savings = total_savings if total_savings > 0 else None

        return EnergyAdvice(
            home_id=home_id,
            recommendations=recommendations,
            summary=advice_data.get("summary", ""),
            estimated_total_annual_savings=estimated_total_annual_savings,
            generated_at=datetime.utcnow(),
            llm_provider=self.llm_provider.get_provider_name()
        )

    def _parse_llm_response(self, response: str) -> dict:
        cleaned_response = response.strip()
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise LLMValidationError(
                f"Failed to parse LLM response as JSON: {str(e)}. "
                f"Response preview: {cleaned_response[:200]}"
            )

    async def validate_provider(self) -> bool:
        return await self.llm_provider.health_check()
