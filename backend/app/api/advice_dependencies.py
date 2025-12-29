from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SQLAlchemyHomeRepository
from app.infrastructure.llm.factory import LLMProviderFactory
from app.application.advice_service import EnergyAdviceService
from fastapi import Depends


def get_llm_provider():
    return LLMProviderFactory.create_provider()


def get_advice_service(
    db: Session = Depends(get_db),
    llm_provider = Depends(get_llm_provider)
) -> EnergyAdviceService:
    repository = SQLAlchemyHomeRepository(db)
    return EnergyAdviceService(repository, llm_provider)
