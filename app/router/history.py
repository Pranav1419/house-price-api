from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/predictions", tags=["history"])


@router.get("", response_model=list[schemas.PredictionRecord])
def list_predictions(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.PredictionLog)
        .order_by(models.PredictionLog.id.desc())   # newest first
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/{prediction_id}", response_model=schemas.PredictionRecord)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    record = db.get(models.PredictionLog, prediction_id)
    if not record:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return record

@router.delete("/{prediction_id}", response_model=schemas.deletePredictionResponse)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    record = db.get(models.PredictionLog, prediction_id)
    if not record:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(record)
    db.commit()
    return schemas.deletePredictionResponse(detail=f"Prediction with id {prediction_id} deleted successfully.")