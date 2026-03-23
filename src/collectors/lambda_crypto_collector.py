import json
import urllib.request
import datetime
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "あなたのバケット名"
FILE_KEY = "crypto/crypto_price.csv"

def lambda_handler(event, context):

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    btc_price = data["bitcoin"]["usd"]
    eth_price = data["ethereum"]["usd"]

    now = datetime.datetime.now()

    row = f"{now},{btc_price},{eth_price}\n"

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        existing_data = obj['Body'].read().decode('utf-8')
    except:
        existing_data = ""

    new_data = existing_data + row

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=FILE_KEY,
        Body=new_data
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }