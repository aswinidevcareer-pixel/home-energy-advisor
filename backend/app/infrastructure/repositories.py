from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities import HomeProfile
from app.domain.repositories import HomeRepository
from app.infrastructure.database import HomeModel
import uuid
from datetime import datetime


class SQLAlchemyHomeRepository(HomeRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, home: HomeProfile) -> HomeProfile:
        home.id = str(uuid.uuid4())
        home.created_at = datetime.utcnow()
        home.updated_at = datetime.utcnow()
        
        db_home = HomeModel(**home.model_dump())
        self.db.add(db_home)
        self.db.commit()
        self.db.refresh(db_home)
        
        return self._to_entity(db_home)

    async def get_by_id(self, home_id: str) -> Optional[HomeProfile]:
        db_home = self.db.query(HomeModel).filter(HomeModel.id == home_id).first()
        if db_home:
            return self._to_entity(db_home)
        return None

    async def update(self, home: HomeProfile) -> HomeProfile:
        home.updated_at = datetime.utcnow()
        db_home = self.db.query(HomeModel).filter(HomeModel.id == home.id).first()
        
        if not db_home:
            raise ValueError(f"Home with id {home.id} not found")
        
        for key, value in home.model_dump(exclude_unset=True).items():
            setattr(db_home, key, value)
        
        self.db.commit()
        self.db.refresh(db_home)
        
        return self._to_entity(db_home)

    async def delete(self, home_id: str) -> bool:
        db_home = self.db.query(HomeModel).filter(HomeModel.id == home_id).first()
        if db_home:
            self.db.delete(db_home)
            self.db.commit()
            return True
        return False

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
            avg_monthly_energy_cost=db_home.avg_monthly_energy_cost,
            zip_code=db_home.zip_code,
            created_at=db_home.created_at,
            updated_at=db_home.updated_at
        )
