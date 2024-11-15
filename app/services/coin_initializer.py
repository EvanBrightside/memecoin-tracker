# file: services/coin_initializer.py
from datetime import datetime, timedelta
from database import SessionLocal
from models import Token  # Предполагается, что Token – это модель для мемкоинов
from services.coingecko_service import fetch_coin_data  # Сервис для сбора данных

def initialize_token_addresses():
    """
    Инициализирует или обновляет список мемкоинов.
    Если список пуст или данные устарели, собирает новые данные.
    """
    db = SessionLocal()
    try:
        last_update = db.query(Token).order_by(Token.updated_at.desc()).first()

        if last_update is None or (datetime.utcnow() - last_update.updated_at) > timedelta(days=30):
            print("Инициализация или обновление списка мемкоинов.")
            
            coin_ids = ["dogecoin", "shiba-inu"]  # Можно расширить список
            coin_data = fetch_coin_data(coin_ids)  # Получаем данные из CoinGecko

            db.query(Token).delete()
            db.commit()

            for coin in coin_data:
                token = Token(
                    name=coin["name"],
                    symbol=coin["symbol"],
                    address=coin["address"],
                    updated_at=datetime.utcnow()
                )
                db.add(token)
            db.commit()
            print("Список мемкоинов успешно обновлен.")
        else:
            print("Список мемкоинов актуален, обновление не требуется.")
    finally:
        db.close()
