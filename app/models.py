from sqlalchemy import Column, DateTime, Float, Integer, func

from .database import Base

class PredictionLog(Base):
    __tablename__ = "house_price_predictions"

    id = Column(Integer, primary_key=True)
    area_sqft = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    age_years = Column(Integer, nullable=False)
    distance_city_km = Column(Float, nullable=False)
    predicted_price = Column(Float(53), nullable=False)
    created_at = Column(DateTime, server_default=func.now())