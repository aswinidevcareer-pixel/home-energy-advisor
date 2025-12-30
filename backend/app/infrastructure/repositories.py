from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.domain.entities import HomeProfile
from app.domain.repositories import HomeRepository
from app.domain.exceptions import DomainError
from app.infrastructure.database import HomeModel
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SQLAlchemyHomeRepository(HomeRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, home: HomeProfile) -> HomeProfile:
        """Create a new home profile in the database."""
        home.id = str(uuid.uuid4())
        home.created_at = datetime.utcnow()
        home.updated_at = datetime.utcnow()
        
        try:
            db_home = HomeModel(**home.model_dump())
            self.db.add(db_home)
            self.db.commit()
            self.db.refresh(db_home)
            return self._to_entity(db_home)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error creating home: {str(e)}", exc_info=True)
            raise DomainError(f"Failed to create home profile") from e

    async def get_by_id(self, home_id: str) -> Optional[HomeProfile]:
        """Retrieve a home profile by ID."""
        try:
            db_home = self.db.query(HomeModel).filter(HomeModel.id == home_id).first()
            return self._to_entity(db_home) if db_home else None
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching home {home_id}: {str(e)}", exc_info=True)
            raise DomainError(f"Failed to retrieve home profile") from e

    async def update(self, home: HomeProfile) -> HomeProfile:
        """Update an existing home profile."""
        home.updated_at = datetime.utcnow()
        
        try:
            db_home = self.db.query(HomeModel).filter(HomeModel.id == home.id).first()
            
            if not db_home:
                raise DomainError(f"Home with id {home.id} not found")
            
            for key, value in home.model_dump(exclude_unset=True).items():
                setattr(db_home, key, value)
            
            self.db.commit()
            self.db.refresh(db_home)
            return self._to_entity(db_home)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error updating home {home.id}: {str(e)}", exc_info=True)
            raise DomainError(f"Failed to update home profile") from e

    async def delete(self, home_id: str) -> bool:
        """Delete a home profile by ID."""
        try:
            db_home = self.db.query(HomeModel).filter(HomeModel.id == home_id).first()
            if db_home:
                self.db.delete(db_home)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error deleting home {home_id}: {str(e)}", exc_info=True)
            raise DomainError(f"Failed to delete home profile") from e

    def _to_entity(self, db_home: HomeModel) -> HomeProfile:
        return HomeProfile(
            id=db_home.id,
            size_sqft=db_home.size_sqft,
            age_years=db_home.age_years,
            heating_type=db_home.heating_type,
            insulation_type=db_home.insulation_type,
            window_type=db_home.window_type,
            num_floors=db_home.num_floors,
            num_occupants=db_home.num_occupants,
            has_basement=db_home.has_basement,
            has_attic=db_home.has_attic,
            has_solar_panels=db_home.has_solar_panels,
            has_smart_thermostat=db_home.has_smart_thermostat,
            # Advanced - Location & Climate
            country=db_home.country,
            zip_code=db_home.zip_code,
            climate_zone=db_home.climate_zone,
            # Advanced - Energy Details
            primary_energy_source=db_home.primary_energy_source,
            avg_monthly_energy_cost=db_home.avg_monthly_energy_cost,
            avg_monthly_kwh=db_home.avg_monthly_kwh,
            hvac_age_years=db_home.hvac_age_years,
            # Advanced - Building Characteristics
            roof_type=db_home.roof_type,
            roof_age_years=db_home.roof_age_years,
            # Advanced - Preferences
            budget_range=db_home.budget_range,
            planning_to_sell_years=db_home.planning_to_sell_years,
            created_at=db_home.created_at,
            updated_at=db_home.updated_at
        )
