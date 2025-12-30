import json
import logging
from datetime import datetime
from typing import Optional
from app.domain.entities import HomeProfile
from app.domain.value_objects import EnergyAdvice, Recommendation
from app.domain.repositories import HomeRepository
from app.domain.exceptions import HomeNotFoundError, LLMValidationError
from app.infrastructure.llm.base import LLMProvider
from app.application.prompt_builder import EnergyAdvicePromptBuilder

# Configure logger
logger = logging.getLogger(__name__)


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
            logger.warning(f"Home not found: {home_id}")
            raise HomeNotFoundError(home_id)

        prompt = self.prompt_builder.build_prompt(home)
        
        logger.info(f"Generating energy advice for home: {home_id}")
        
        try:
            llm_response = await self.llm_provider.generate_completion(
                prompt=prompt,
                temperature=0.7,
                response_format=EnergyAdvice.model_json_schema(),
                max_tokens=4000
            )

            logger.debug(f"LLM Response received for home {home_id}: {llm_response[:200]}...")
            
            advice_data = self._parse_llm_response(llm_response, home_id)

            # Process recommendations and build EnergyAdvice
            recommendations = self._process_recommendations(advice_data.get("recommendations", []))
            estimated_total_annual_savings = self._calculate_total_savings(
                advice_data.get("estimated_total_annual_savings"),
                recommendations
            )
        except LLMValidationError:
            # LLM validation errors are already logged and user-friendly, just re-raise
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating advice for home {home_id}: {str(e)}", exc_info=True)
            raise

        return EnergyAdvice(
            home_id=home_id,
            recommendations=recommendations,
            summary=advice_data.get("summary", ""),
            estimated_total_annual_savings=estimated_total_annual_savings,
            generated_at=datetime.utcnow(),
            llm_provider=self.llm_provider.get_provider_name()
        )

    def _process_recommendations(self, recommendations_data: list) -> list[Recommendation]:
        """Process and validate recommendation data from LLM response."""
        recommendations = []
        
        for rec_data in recommendations_data:
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
            
            recommendations.append(Recommendation(**rec_data))
        
        return recommendations

    def _calculate_total_savings(
        self, 
        llm_provided_total: Optional[float],
        recommendations: list[Recommendation]
    ) -> Optional[float]:
        """Calculate total annual savings from recommendations if not provided by LLM."""
        if llm_provided_total is not None:
            return llm_provided_total
        
        # Sum up all individual recommendation savings
        total_savings = sum(
            rec.estimated_savings_annual 
            for rec in recommendations 
            if rec.estimated_savings_annual is not None
        )
        
        # Return calculated total if available, otherwise None
        return total_savings if total_savings > 0 else None

    def _parse_llm_response(self, response: str, home_id: str = None) -> dict:
        """Parse LLM response with detailed error logging."""
        cleaned_response = response.strip()
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error - Line: {e.lineno}, Column: {e.colno}, Message: {e.msg}"
            if home_id:
                logger.error(f"Failed to parse LLM response for home {home_id}: {error_msg}")
                logger.debug(f"Raw LLM response causing error: {cleaned_response}")
            else:
                logger.error(f"Failed to parse LLM response: {error_msg}")
                logger.debug(f"Raw response: {cleaned_response}")
            
            # Re-raise with user-friendly message (technical details already logged)
            raise LLMValidationError("Unable to process AI response. Please try again.")
