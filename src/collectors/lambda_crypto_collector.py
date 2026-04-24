import json
import urllib.request
import datetime
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "investment-dashboard-data-shimizu"

def lambda_handler(event, context):

    # ▼ Crypto（BTC / ETH）
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    with urllib.request.urlopen(crypto_url) as response:
        crypto_data = json.loads(response.read().decode())

    btc_price = crypto_data["bitcoin"]["usd"]
    eth_price = crypto_data["ethereum"]["usd"]

    # ▼ USDJPY（為替）
    fx_url = "https://api.exchangerate-api.com/v4/latest/USD"

    with urllib.request.urlopen(fx_url) as response:
        fx_data = json.loads(response.read().decode())

    usd_jpy = fx_data["rates"]["JPY"]

    # ▼ まとめる（ここが重要）
    price_dict = {
        "BTC": btc_price,
        "ETH": eth_price,
        "USDJPY": usd_jpy
    }

    now = datetime.datetime.now()

    # ▼ ループでS3保存
    for symbol, price in price_dict.items():

        row = f"{now},{price}\n"
        key = f"{symbol}/data.csv"

        try:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            existing_data = obj['Body'].read().decode('utf-8')
        except:
            existing_data = ""

        new_data = existing_data + row

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=new_data
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }