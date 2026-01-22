import pandas as pd
import hashlib

class FeatureProvider:
    def __init__(self):
        # Mock feature store
        self.X = pd.read_csv("data/processed/X_test.csv")
        self.y = pd.read_csv("data/processed/y_test.csv")

        # Store indices of known fraud rows (for testing)
        self.fraud_indices = self.y[self.y["Class"] == 1].index.tolist()

    def get_entities_for_transaction(self, transaction_id: str):
        """
        Deterministic feature lookup.

        - Same transaction_id → same feature row
        - Special keyword allows forcing fraud for testing
        """

        # 🔴 TEST TRIGGER (for demos & validation)
        if "fraud" in transaction_id.lower():
            fraud_idx = self.fraud_indices[0]
            return self.X.iloc[[fraud_idx]]

        # 🔒 Deterministic mapping
        hash_val = int(
            hashlib.sha256(transaction_id.encode()).hexdigest(),
            16
        )
        stable_idx = hash_val % len(self.X)

        return self.X.iloc[[stable_idx]]
