import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
VS_CURRENCY = "usd"

def fetch_coin_data(coin_ids):
    response = requests.get(
        COINGECKO_API_URL,
        params={"vs_currency": VS_CURRENCY, "ids": ",".join(coin_ids)},
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе к CoinGecko API: {response.status_code}")
        return []

def fetch_historical_data(coin_id: str, days: int):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["prices"]  # Возвращаем только данные о цене
    else:
        return {"error": "Не удалось получить данные"}
