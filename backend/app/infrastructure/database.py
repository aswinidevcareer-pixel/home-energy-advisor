from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class HomeModel(Base):
    __tablename__ = "homes"

    id = Column(String, primary_key=True, index=True)
    # Basic Information
    size_sqft = Column(Integer, nullable=False)
    age_years = Column(Integer, nullable=False)
    heating_type = Column(String, nullable=False)
    insulation_type = Column(String, nullable=False)
    window_type = Column(String, nullable=False)
    num_floors = Column(Integer, nullable=False)
    num_occupants = Column(Integer, nullable=False)
    has_basement = Column(Boolean, default=False)
    has_attic = Column(Boolean, default=False)
    has_solar_panels = Column(Boolean, default=False)
    has_smart_thermostat = Column(Boolean, default=False)
    
    # Advanced - Location & Climate
    country = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    climate_zone = Column(String, nullable=True)
    
    # Advanced - Energy Details
    primary_energy_source = Column(String, nullable=True)
    avg_monthly_energy_cost = Column(Float, nullable=True)
    avg_monthly_kwh = Column(Float, nullable=True)
    hvac_age_years = Column(Integer, nullable=True)
    
    # Advanced - Building Characteristics
    roof_type = Column(String, nullable=True)
    roof_age_years = Column(Integer, nullable=True)
    
    # Advanced - Preferences
    budget_range = Column(String, nullable=True)
    planning_to_sell_years = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
