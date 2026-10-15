from fastapi import APIRouter,Depends
from .. import ml, schemas, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=["predict"])

@router.post("/predict", response_model=schemas.PredictionOut)
def predict(features: schemas.HouseFeatures, db: Session = Depends(get_db)):
    data = features.model_dump()
    price = ml.predict_price(data)
    db.add(models.PredictionLog(
        area_sqft=features.Area_sqft,
        bedrooms=features.Bedrooms,
        bathrooms=features.Bathrooms,
        age_years=features.Age_years,
        distance_city_km=features.Distance_city_km,
        predicted_price=price,
    ))
    db.commit()
    return {**data, "predicted_price": price}