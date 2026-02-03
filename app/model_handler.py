import joblib
import pandas as pd

class ModelHandler:
    def __init__(self, model_path: str):
        # Load model ONCE when server starts
        self.model = joblib.load(model_path)

    def predict(self, features: pd.DataFrame):
        """
        Input: DataFrame with the exact columns the model was trained on
        Output: (prediction, probability)
        """
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]

        return int(prediction), float(probability)
