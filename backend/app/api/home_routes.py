from fastapi import APIRouter, Depends, HTTPException, status
import logging
from app.application.home_service import HomeService
from app.application.home_dtos import CreateHomeRequest, HomeResponse, ErrorResponse
from app.api.home_dependencies import get_home_service

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/homes", tags=["homes"])


@router.post(
    "",
    response_model=HomeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Home profile created successfully",
            "model": HomeResponse
        },
        400: {
            "description": "Invalid request data",
            "model": ErrorResponse
        },
        422: {
            "description": "Validation error",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal Server Error",
            "model": ErrorResponse
        }
    },
    summary="Create a new home profile",
    description="Create a new home profile with energy-related characteristics for generating personalized energy efficiency recommendations."
)
async def create_home(
    request: CreateHomeRequest,
    service: HomeService = Depends(get_home_service)
) -> HomeResponse:
    try:
        return await service.create_home(request)
    except ValueError as e:
        logger.warning(f"Invalid home data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid home profile data. Please check your inputs and try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error creating home: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create home profile. Please try again later."
        )


@router.get(
    "/{home_id}",
    response_model=HomeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Home profile retrieved successfully",
            "model": HomeResponse
        },
        404: {
            "description": "Home profile not found",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal Server Error",
            "model": ErrorResponse
        }
    },
    summary="Get a home profile by ID",
    description="Retrieve a specific home profile using its unique identifier."
)
async def get_home(
    home_id: str,
    service: HomeService = Depends(get_home_service)
) -> HomeResponse:
    try:
        home = await service.get_home(home_id)
        if not home:
            logger.warning(f"Home not found: {home_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Home profile not found."
            )
        return home
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving home {home_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve home profile. Please try again later."
        )
