from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class HouseFeatures(BaseModel):
    Area_sqft: float = Field(gt=0, le=100000)
    Bedrooms: int = Field(ge=1, le=10)
    Bathrooms: int = Field(ge=1, le=10)
    Age_years: int = Field(ge=0, le=100)
    Distance_city_km: float = Field(ge=0, le=1000)

class PredictionOut(HouseFeatures):
    predicted_price: float




class PredictionRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    area_sqft: float
    bedrooms: int
    bathrooms: int
    age_years: int
    distance_city_km: float
    predicted_price: float
    created_at: datetime

class deletePredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    detail: str