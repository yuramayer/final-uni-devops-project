import json
import uuid
from datetime import datetime

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException

from .ml_model import SimpleLogisticModel
from .schemas import PredictRequest, PredictResponse, PredictionEvent
from .settings import settings

app = FastAPI()
ml_model = SimpleLogisticModel()
redis_client = None
CHANNEL = "prediction_events"


@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    try:
        await redis_client.ping()
    except Exception as e:
        print("Redis error:", e)


@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    if redis_client is None:
        raise HTTPException(500, "Redis unavailable")

    features = {"feature_1": req.feature_1, "feature_2": req.feature_2}
    probability = ml_model.predict_proba(features)
    predicted_class = ml_model.predict_class(features)
    request_id = str(uuid.uuid4())

    event = PredictionEvent(
        request_id=request_id,
        features=features,
        probability=probability,
        predicted_class=predicted_class,
        timestamp=datetime.utcnow(),
    )

    await redis_client.publish(CHANNEL, json.dumps(event.model_dump(), default=str))

    return PredictResponse(
        request_id=request_id,
        probability=probability,
        predicted_class=predicted_class,
    )


@app.get("/health")
def health():
    return {"status": "ok"}
