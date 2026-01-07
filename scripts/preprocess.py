import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def preprocess():
    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv("data/raw/creditcard.csv")

    # 2. Engineering: The 'Time' and 'Amount' features are not scaled like V1-V28
    # We use StandardScaler to give them a mean of 0 and variance of 1
    print("Scaling features...")
    scaler = StandardScaler()
    df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    
    # We drop the original Time and Amount
    df.drop(['Time', 'Amount'], axis=1, inplace=True)

    # 3. Splitting: 80% Training, 20% Testing
    print("Splitting data...")
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Save processed files
    os.makedirs("data/processed", exist_ok=True)
    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_test.to_csv("data/processed/X_test.csv", index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)
    print("Preprocessing complete. Files saved in data/processed/")

if __name__ == "__main__":
    preprocess()