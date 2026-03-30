import json
import urllib.request
import datetime
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "investment-dashboard-data-shimizu"
# 削除してOK（使わなくなる）
# FILE_KEY = "crypto/crypto_price.csv"

def lambda_handler(event, context):

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    # ▼ ① symbolごとにまとめる（超重要）
    price_dict = {
        "BTC": data["bitcoin"]["usd"],
        "ETH": data["ethereum"]["usd"]
    }

    now = datetime.datetime.now()

    # ▼ ② ループで処理
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