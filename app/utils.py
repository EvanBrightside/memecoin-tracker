from datetime import datetime, timedelta
import numpy as np

def format_transaction_data(data):
    """
    Функция для форматирования данных транзакции, полученных из блокчейна Solana,
    в удобный для хранения и анализа вид.
    """
    formatted_data = []
    for transaction in data:
        formatted_data.append({
            "wallet_address": transaction["wallet_address"],
            "amount": transaction["amount"],
            "timestamp": datetime.fromtimestamp(transaction["timestamp"])
        })
    return formatted_data

def calculate_growth_rate(current_price, previous_price):
    """
    Функция для расчета процентного роста или снижения цены токена.
    """
    if previous_price == 0:
        return 0
    return ((current_price - previous_price) / previous_price) * 100

def preprocess_data_for_model(transactions):
    """
    Функция для предобработки данных транзакций перед подачей их в модель ИИ.
    Возвращает массив numpy для использования в модели.
    """
    # Пример: вычисление средней суммы транзакций за последние 24 часа
    recent_transactions = [
        tx["amount"] for tx in transactions if tx["timestamp"] >= datetime.utcnow() - timedelta(days=1)
    ]
    mean_transaction_amount = np.mean(recent_transactions) if recent_transactions else 0
    return np.array([mean_transaction_amount])

def fetch_token_price_data(token_id):
    """
    Функция для получения данных по цене токена из базы данных
    за последние N дней для использования в модели ИИ.
    """
    # Здесь будет логика для запроса в БД
    pass
