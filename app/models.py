from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Модель для токенов (мемкоинов)
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)          # Название токена
    symbol = Column(String, unique=True, index=True)        # Символ токена
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата добавления токена
    current_price = Column(Float)                           # Текущая цена токена
    volume = Column(Float)                                  # Текущий объем торгов токена

    # Отношение с таблицей транзакций
    transactions = relationship("Transaction", back_populates="token")

# Модель для хранения транзакций
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey("tokens.id"))  # Связь с таблицей Token
    timestamp = Column(DateTime, default=datetime.utcnow)  # Время транзакции
    wallet_address = Column(String)                       # Адрес кошелька
    amount = Column(Float)                                # Количество токенов

    # Связь с токеном
    token = relationship("Token", back_populates="transactions")

# Модель для хранения прогнозов
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey("tokens.id"))  # Связь с таблицей Token
    prediction_date = Column(DateTime, default=datetime.utcnow)  # Дата прогноза
    predicted_growth = Column(Float)                              # Прогнозируемый рост (в процентах)

    # Связь с токеном
    token = relationship("Token")
