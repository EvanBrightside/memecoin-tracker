from solana.rpc.api import Client
from datetime import datetime, timedelta
import numpy as np

client = Client("https://api.mainnet-beta.solana.com")

# Пороговые значения для "крупных" кошельков
LARGE_TRANSACTION_THRESHOLD = 10000  # Примерный объем токенов
FREQUENT_TRANSACTION_THRESHOLD = 10  # Минимум транзакций с новым мемкоином за месяц

def fetch_recent_transactions(token_address):
    last_month = datetime.now() - timedelta(days=30)
    signatures = client.get_confirmed_signatures_for_address2(token_address, limit=1000)  # Ограничьте до 1000 записей или по необходимости

    recent_transactions = []
    for signature_info in signatures["result"]:
        block_time = signature_info.get("blockTime")
        if block_time and datetime.utcfromtimestamp(block_time) > last_month:
            # Получаем детали транзакции
            transaction = client.get_confirmed_transaction(signature_info["signature"])
            recent_transactions.append(transaction)

    return recent_transactions

def analyze_wallets():
    transactions = fetch_recent_transactions()
    wallet_stats = {}

    for tx in transactions:
        sender = tx.get("sender")
        recipient = tx.get("recipient")
        amount = tx.get("amount")

        if sender not in wallet_stats:
            wallet_stats[sender] = {"total_amount": 0, "transaction_count": 0}
        wallet_stats[sender]["total_amount"] += amount
        wallet_stats[sender]["transaction_count"] += 1

        if recipient not in wallet_stats:
            wallet_stats[recipient] = {"total_amount": 0, "transaction_count": 0}
        wallet_stats[recipient]["total_amount"] += amount
        wallet_stats[recipient]["transaction_count"] += 1

    large_wallets = {
        wallet: stats
        for wallet, stats in wallet_stats.items()
        if stats["total_amount"] > LARGE_TRANSACTION_THRESHOLD
        and stats["transaction_count"] > FREQUENT_TRANSACTION_THRESHOLD
    }

    return large_wallets
