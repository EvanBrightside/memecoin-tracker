from solana.rpc.api import Client

def initialize_blockchain_monitor():
    """
    Инициализирует клиент Solana для мониторинга блокчейна.
    """
    client = Client("https://api.mainnet-beta.solana.com")
    return client

def get_recent_transactions():
    client = Client("https://api.mainnet-beta.solana.com")
    transactions = client.get_recent_blockhash()

    return transactions

def fetch_token_data(token_address):
    """
    Получает данные о токене по его адресу.
    Эта функция делает запрос в Solana и возвращает информацию о токене.
    """
    client = Client("https://api.mainnet-beta.solana.com")
    # Пример вызова API для получения данных о конкретном токене
    response = client.get_account_info(token_address)
    return response