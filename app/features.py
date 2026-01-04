class FeatureProvider:
    def __init__(self):
        # This is where we will initialize the Redis client in Week 3
        pass

    def get_user_features(self, transaction_id: str):
        # Mocking a feature lookup
        # In a real system, this would fetch 'average_spend_24h', etc.
        return {
            "avg_spend_24h": 120.50,
            "failed_attempts_today": 0
        }