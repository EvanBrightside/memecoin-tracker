from solana.rpc.api import Client
from datetime import datetime, timezone, timedelta
from services.wallet_analysis import fetch_recent_transactions

client = Client("https://api.mainnet-beta.solana.com")

LARGE_TRANSACTION_THRESHOLD = 10000
FREQUENT_TRANSACTION_THRESHOLD = 10

def initialize_blockchain_monitor():
    client = Client("https://api.mainnet-beta.solana.com")
    return client

def get_recent_transactions():
    client = Client("https://api.mainnet-beta.solana.com")
    transactions = client.get_recent_blockhash()

    return transactions

def fetch_token_data(token_address):
    client = Client("https://api.mainnet-beta.solana.com")
    response = client.get_account_info(token_address)

    return response

def fetch_new_tokens(last_n_days=30):
    client = Client("https://api.mainnet-beta.solana.com")
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(days=last_n_days)
    new_tokens = client.get_new_tokens(start_time)

    return new_tokens

def analyze_large_wallets(token_address):
    transactions = fetch_recent_transactions(token_address)
    
    wallet_stats = {}

    for tx in transactions:
        # Проход по каждой операции в транзакции
        for instruction in tx["result"]["transaction"]["message"]["instructions"]:
            if "parsed" in instruction:
                info = instruction["parsed"]["info"]
                sender = info.get("source")
                recipient = info.get("destination")
                amount = int(info.get("amount", 0))

                # Анализ отправителя
                if sender:
                    if sender not in wallet_stats:
                        wallet_stats[sender] = {"total_amount": 0, "transaction_count": 0}
                    wallet_stats[sender]["total_amount"] += amount
                    wallet_stats[sender]["transaction_count"] += 1

                # Анализ получателя
                if recipient:
                    if recipient not in wallet_stats:
                        wallet_stats[recipient] = {"total_amount": 0, "transaction_count": 0}
                    wallet_stats[recipient]["total_amount"] += amount
                    wallet_stats[recipient]["transaction_count"] += 1

    # Фильтруем крупные кошельки
    large_wallets = {
        wallet: stats
        for wallet, stats in wallet_stats.items()
        if stats["total_amount"] > LARGE_TRANSACTION_THRESHOLD
        and stats["transaction_count"] > FREQUENT_TRANSACTION_THRESHOLD
    }

    return large_wallets