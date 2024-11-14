from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.blockchain import fetch_token_data
from models import Token
from services.coingecko_service import fetch_coin_data
from services.coingecko_service import fetch_historical_data
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/tokens/market_data")
async def get_tokens_market_data():
    coin_ids = ["dogecoin", "shiba-inu"]
    market_data = fetch_coin_data(coin_ids)

    for token in market_data:
        coin_id = token["id"]
        historical_data = fetch_historical_data(coin_id, 7)

        if isinstance(historical_data, list) and all(isinstance(day, list) for day in historical_data):
            token['price_history'] = [day[1] for day in historical_data]  # day[1] - это цена в каждом подсписке
        else:
            token['price_history'] = []  # Добавляем пустой список, если данные неверные

    return market_data

@router.get("/tokens/{coin_id}/historical_data")
async def get_historical_data(coin_id: str):
    days = 7
    historical_data = fetch_historical_data(coin_id, days)
    return historical_data
