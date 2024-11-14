# scripts/init_db.py
from database import Base, engine, SessionLocal
from models import Token, Transaction
from datetime import datetime
import random

def init_db():
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Таблицы созданы.")
            break
        except OperationalError as e:
            print("База данных пока не готова, повтор через 5 секунд...")
            retries -= 1
            time.sleep(5)
    if retries == 0:
        print("Не удалось подключиться к базе данных. Проверьте настройки.")

def add_sample_data():
    """
    Добавление тестовых данных в базу для проверки работы приложения.
    """
    db = SessionLocal()

    # Пример добавления нескольких мемкоинов, если они еще не существуют
    tokens_data = [
        {"name": "DogeCoin", "symbol": "DOGE", "current_price": 0.1, "volume": 1000000},
        {"name": "ShibaInu", "symbol": "SHIB", "current_price": 0.00001, "volume": 500000},
    ]

    for token_data in tokens_data:
        # Проверяем, существует ли токен с таким символом
        token = db.query(Token).filter_by(symbol=token_data["symbol"]).first()
        if not token:
            # Если токен не найден, добавляем его
            new_token = Token(
                name=token_data["name"],
                symbol=token_data["symbol"],
                current_price=token_data["current_price"],
                volume=token_data["volume"],
                created_at=datetime.utcnow()
            )
            db.add(new_token)
            print(f"Добавлен токен: {token_data['name']}")

    db.commit()

    # Пример добавления транзакций для каждого токена
    tokens = db.query(Token).all()
    for token in tokens:
        for _ in range(10):  # создаём 10 транзакций для каждого токена
            transaction = Transaction(
                token_id=token.id,
                wallet_address=f"wallet_{random.randint(1, 1000)}",
                amount=random.uniform(100, 1000),
                timestamp=datetime.utcnow()
            )
            db.add(transaction)

    db.commit()
    db.close()
    print("Тестовые данные добавлены.")

if __name__ == "__main__":
    init_db()
    add_sample_data()
