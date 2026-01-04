from fastapi import FastAPI, Depends
from .schemas import Transaction, PredictionResponse
from .features import FeatureProvider

app = FastAPI(title="SentinelML - Fraud Detection Service")

# Dependency Injection: We create one instance of the provider
def get_feature_provider():
    return FeatureProvider()

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_version": "0.1.0-mock"}

@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: Transaction, provider: FeatureProvider = Depends(get_feature_provider)):
    # 1. Fetch features (This is our abstraction at work!)
    features = provider.get_user_features(transaction.transaction_id)
    
    # 2. Mock Logic (We will replace this with XGBoost in Week 2)
    # For now, if amount > 10000, we'll call it fraud for testing
    is_fraud = transaction.amount > 10000
    
    return PredictionResponse(
        is_fraud=is_fraud,
        confidence=0.99 if is_fraud else 0.5,
        reasons=["High transaction amount"] if is_fraud else ["Normal behavior"]
    )