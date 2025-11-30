from datetime import datetime
from typing import Dict
from pydantic import BaseModel


class PredictRequest(BaseModel):
    feature_1: float
    feature_2: float


class PredictResponse(BaseModel):
    request_id: str
    probability: float
    predicted_class: int


class PredictionEvent(BaseModel):
    request_id: str
    features: Dict[str, float]
    probability: float
    predicted_class: int
    timestamp: datetime
