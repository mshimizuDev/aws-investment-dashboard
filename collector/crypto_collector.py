import requests
import datetime

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

response = requests.get(url)
data = response.json()

btc_price = data["bitcoin"]["usd"]
eth_price = data["ethereum"]["usd"]

now = datetime.datetime.now()

with open("../data/crypto_price.csv", "a") as f:
    f.write(f"{now},{btc_price},{eth_price}\n")

print("BTC:", btc_price, "ETH:", eth_price)