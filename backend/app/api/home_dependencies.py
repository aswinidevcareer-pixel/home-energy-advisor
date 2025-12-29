from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SQLAlchemyHomeRepository
from app.application.home_service import HomeService
from fastapi import Depends


def get_home_repository(db: Session = Depends(get_db)) -> SQLAlchemyHomeRepository:
    return SQLAlchemyHomeRepository(db)


def get_home_service(repository: SQLAlchemyHomeRepository = Depends(get_home_repository)) -> HomeService:
    return HomeService(repository)
