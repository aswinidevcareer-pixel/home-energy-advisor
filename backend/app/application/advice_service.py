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
        
        recommendations = [
            Recommendation(**rec) for rec in advice_data.get("recommendations", [])
        ]
        
        return EnergyAdvice(
            home_id=home_id,
            recommendations=recommendations,
            summary=advice_data.get("summary", ""),
            estimated_total_annual_savings=advice_data.get("estimated_total_annual_savings"),
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
