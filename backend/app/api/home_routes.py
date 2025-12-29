from fastapi import APIRouter, Depends, HTTPException, status
from app.application.home_service import HomeService
from app.application.home_dtos import CreateHomeRequest, HomeResponse, ErrorResponse
from app.api.home_dependencies import get_home_service

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the home profile"
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
    home = await service.get_home(home_id)
    if not home:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Home profile with id '{home_id}' not found"
        )
    return home
