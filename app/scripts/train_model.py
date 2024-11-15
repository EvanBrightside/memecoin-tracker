import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from services.ml_model import train_new_model
from database import SessionLocal
from models import Transaction, Token
from services.twitter_service import fetch_tweets_for_token
from services.blockchain import analyze_large_wallets

def fetch_training_data():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    data = []
    for tx in transactions:
        token_name = tx.token.name
        tweets = fetch_tweets_for_token(token_name)
        large_wallet_transactions = analyze_large_wallets(tx.token.token_address)
        
        data.append({
            "token_id": tx.token_id,
            "amount": tx.amount,
            "timestamp": tx.timestamp.timestamp(),
            "num_tweets": len(tweets),
            "large_wallet_volume": len(large_wallet_transactions),
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
