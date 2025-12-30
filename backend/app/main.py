from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import sys
from app.config import settings
from app.infrastructure.database import init_db
from app.api.home_routes import router as homes_router
from app.api.advice_routes import router as advice_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered home energy efficiency advisor API",
    openapi_tags=[
        {
            "name": "homes",
            "description": "Operations related to home profiles"
        },
        {
            "name": "energy-advice",
            "description": "AI-powered energy efficiency recommendations"
        },
        {
            "name": "health",
            "description": "API health and status endpoints"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append(f"{field}: {error['msg']}")
    
    # Log validation errors
    logger.warning(f"Validation error on {request.url.path}: {errors}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Please check your input and try again."
        }
    )


@app.on_event("startup")
def on_startup():
    logger.info("Starting Home Energy Advisor API...")
    init_db()
    logger.info("Database initialized successfully")


@app.get("/", tags=["health"])
async def root():
    return {
        "message": "Home Energy Advisor API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


app.include_router(homes_router, prefix=settings.API_V1_PREFIX)
app.include_router(advice_router, prefix=settings.API_V1_PREFIX)
