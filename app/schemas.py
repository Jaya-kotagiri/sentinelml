from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    location: str
    timestamp: datetime
    merchant_category: str

class PredictionResponse(BaseModel):
    is_fraud: bool
    confidence: float
    # We add this now so our 'Armor' phase is easier later
    reasons: Optional[List[str]] = None