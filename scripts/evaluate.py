import pandas as pd
import joblib
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve

def evaluate():
    # 1. Load Data and Model
    X_test = pd.read_csv("data/processed/X_test.csv")
    y_test = pd.read_csv("data/processed/y_test.csv")
    model = joblib.load("models/model.pkl")

    # 2. Predict
    predictions = model.predict(X_test)
    
    # 3. Generate Metrics 
    report = classification_report(y_test, predictions, output_dict=True) #Recall & Precision
    
    # 4. Create Evaluation Folder
    os.makedirs("eval", exist_ok=True)
    
    # 5. Save Metrics JSON (DVC will track this)
    with open("eval/metrics.json", "w") as f:
        json.dump(report, f, indent=4)

    # 6. Plot Confusion Matrix
    cm = confusion_matrix(y_test, predictions) #counts
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Fraud Detection Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig("eval/confusion_matrix.png")
    print("Evaluation complete. Check the 'eval' folder for results.")

if __name__ == "__main__":
    evaluate()