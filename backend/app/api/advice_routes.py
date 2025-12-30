from fastapi import APIRouter, Depends, HTTPException, status
import logging
from app.application.advice_service import EnergyAdviceService
from app.application.advice_dtos import EnergyAdviceResponse
from app.api.advice_dependencies import get_advice_service
from app.application.home_dtos import ErrorResponse
from app.domain.exceptions import (
    HomeNotFoundError,
    LLMConnectionError,
    LLMTimeoutError,
    LLMServiceUnavailableError,
    LLMValidationError
)

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/homes", tags=["energy-advice"])


@router.post(
    "/{home_id}/advice",
    response_model=EnergyAdviceResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Energy advice generated successfully",
            "model": EnergyAdviceResponse
        },
        404: {
            "description": "Home profile not found",
            "model": ErrorResponse
        },
        422: {
            "description": "LLM response validation failed",
            "model": ErrorResponse
        },
        503: {
            "description": "LLM service unavailable or connection error",
            "model": ErrorResponse
        },
        504: {
            "description": "LLM request timeout",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    },
    summary="Generate energy-saving recommendations"
)
async def generate_energy_advice(
    home_id: str,
    service: EnergyAdviceService = Depends(get_advice_service)
) -> EnergyAdviceResponse:
    try:
        advice = await service.generate_advice(home_id)
        return EnergyAdviceResponse(
            home_id=advice.home_id,
            recommendations=[
                {
                    "title": rec.title,
                    "description": rec.description,
                    "priority": rec.priority,
                    "category": rec.category,
                    "estimated_savings_annual": rec.estimated_savings_annual,
                    "estimated_cost": rec.estimated_cost,
                    "payback_period_years": rec.payback_period_years,
                    "implementation_difficulty": rec.implementation_difficulty
                }
                for rec in advice.recommendations
            ],
            summary=advice.summary,
            estimated_total_annual_savings=advice.estimated_total_annual_savings,
            generated_at=advice.generated_at,
            llm_provider=advice.llm_provider
        )
    except HomeNotFoundError as e:
        # Home not found - log and return user-friendly message
        logger.warning(f"Home not found: {e.resource_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Home profile not found. Please create a home profile first."
        )
    except LLMTimeoutError as e:
        # Timeout - log technical details, return user-friendly message
        logger.error(f"LLM timeout for home {home_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI service took too long to respond. Please try again."
        )
    except (LLMConnectionError, LLMServiceUnavailableError) as e:
        # Connection issues - log technical details
        logger.error(f"LLM service unavailable for home {home_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is temporarily unavailable. Please try again in a few moments."
        )
    except LLMValidationError as e:
        # Validation errors - already logged in service, just return user-friendly message
        logger.error(f"LLM validation error for home {home_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to generate recommendations at this time. Please try again."
        )
    except Exception as e:
        # Unexpected errors - log full details, return generic message
        logger.error(f"Unexpected error generating advice for home {home_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Our team has been notified. Please try again later."
        )