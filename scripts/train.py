import pandas as pd
import xgboost as xgb
import joblib
import os

def train():
    # Load data
    X_train = pd.read_csv("data/processed/X_train.csv")
    y_train = pd.read_csv("data/processed/y_train.csv").values.ravel()

    print("Training XGBoost model...")

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=580,  # class imbalance handling
        eval_metric="logloss",
        use_label_encoder=False
    )

    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")

    print("Model saved at models/model.pkl")

if __name__ == "__main__":
    train()
