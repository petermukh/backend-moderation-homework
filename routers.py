from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas import PredictionRequest
from services import PredictionService, get_prediction_service


router = APIRouter()


@router.post("/predict", response_model=bool)
def predict(
    advertisement: PredictionRequest,
    service: Annotated[PredictionService, Depends(get_prediction_service)],
) -> bool:
    try:
        return service.predict(advertisement)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
