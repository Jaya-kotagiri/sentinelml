from fastapi import FastAPI
from .schemas import Transaction, PredictionResponse
from .model_handler import ModelHandler
from .features import FeatureProvider
import os

app = FastAPI(title="SentinelML - Fraud Detection Service")

# ---- Load model once (production pattern) ----
MODEL_PATH = "models/model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model not found. Train the model before serving.")

model_handler = ModelHandler(MODEL_PATH)
feature_provider = FeatureProvider()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: Transaction):
    """
    End-to-end inference:
    1. Receive transaction_id
    2. Fetch real model features
    3. Run ML model
    4. Return decision + confidence
    """

    # 1. Feature lookup (mocked feature store)
    features = feature_provider.get_entities_for_transaction(
        transaction.transaction_id
    )

    # 2. Model inference
    is_fraud, confidence = model_handler.predict(features)

    # 3. API response
    return PredictionResponse(
        is_fraud=bool(is_fraud),
        confidence=float(confidence),
        reasons=[
            "High risk PCA signature detected"
        ] if is_fraud else [
            "Transaction matches user profile"
        ]
    )
