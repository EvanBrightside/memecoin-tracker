import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Подключение к базе данных и загрузка данных
from database import SessionLocal
from models import Transaction, Token

def fetch_training_data():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    data = []
    for tx in transactions:
        data.append({
            "token_id": tx.token_id,
            "amount": tx.amount,
            "timestamp": tx.timestamp.timestamp()
        })
    return pd.DataFrame(data)

def train_model():
    data = fetch_training_data()
    
    X = data[["token_id", "amount", "timestamp"]]
    y = data["amount"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Создание каталога "models" при его отсутствии
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/token_growth_model.pkl")
    print("Модель обучена и сохранена.")

if __name__ == "__main__":
    train_model()
