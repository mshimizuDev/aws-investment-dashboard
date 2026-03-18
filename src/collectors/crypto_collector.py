import requests
import datetime

from src.utils.csv_writer import save_to_csv
from src.utils.config import CRYPTO_CSV

def fetch_crypto_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    response = requests.get(url)
    data = response.json()

    btc_price = data["bitcoin"]["usd"]
    eth_price = data["ethereum"]["usd"]

    return btc_price, eth_price


def main():
    btc_price, eth_price = fetch_crypto_price()

    now = datetime.datetime.now()

    row = [now, btc_price, eth_price]

    save_to_csv(CRYPTO_CSV, row)

    print("BTC:", btc_price, "ETH:", eth_price)


if __name__ == "__main__":
    main()