from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Token
from services.blockchain import fetch_token_data, fetch_new_tokens, analyze_large_wallets
from services.coingecko_service import fetch_coin_data
from services.coingecko_service import fetch_historical_data
from services.ml_model import initialize_ml_model
from services.twitter_service import fetch_tweets_for_token
from datetime import datetime, timedelta
import random

router = APIRouter()
ml_model = initialize_ml_model()

@router.get("/tokens/market_data")
async def get_tokens_market_data():
    coin_ids = ["dogecoin", "shiba-inu"]
    market_data = fetch_coin_data(coin_ids)

    for token in market_data:
        coin_id = token["id"]
        historical_data = fetch_historical_data(coin_id, 7)

        if isinstance(historical_data, list) and all(isinstance(day, list) for day in historical_data):
            token['price_history'] = [day[1] for day in historical_data]
        else:
            token['price_history'] = []

    return market_data

@router.get("/tokens/{coin_id}/historical_data")
async def get_historical_data(coin_id: str):
    days = 7
    historical_data = fetch_historical_data(coin_id, days)
    return historical_data

@router.get("/tokens/investment_recommendations")
async def get_investment_recommendations():
    new_tokens = fetch_new_tokens()
    recommendations = []
    
    for token in new_tokens:
        token_data = {
            "num_tweets": len(fetch_tweets_for_token(token['name'])),
            "large_wallet_volume": len(analyze_large_wallets(token['address'])),
            # Дополнительные признаки
        }
        prediction = ml_model.predict(np.array([list(token_data.values())]))[0]
        if prediction > 0.7:  # Пример: порог 0.7 для "положительного прогноза"
            recommendations.append(token)
    
    return recommendations