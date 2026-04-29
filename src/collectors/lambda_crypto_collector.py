import json
import urllib.request
import datetime
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "investment-dashboard-data-shimizu"

def safe_request(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("Request failed:", url, e)
        return None


def lambda_handler(event, context):

    price_dict = {}
    now = datetime.datetime.now()

    # ▼ BTC / ETH（安定）
    crypto_data = safe_request(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    )

    if crypto_data:
        price_dict["BTC"] = crypto_data["bitcoin"]["usd"]
        price_dict["ETH"] = crypto_data["ethereum"]["usd"]

    # ▼ USDJPY（安定）
    fx_data = safe_request(
        "https://api.exchangerate-api.com/v4/latest/USD"
    )

    if fx_data:
        price_dict["USDJPY"] = fx_data["rates"]["JPY"]

    # ▼ SP500（不安定）
    sp_data = safe_request(
        "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5EGSPC"
    )

    if sp_data and sp_data.get("quoteResponse", {}).get("result"):
        try:
            price_dict["SP500"] = sp_data["quoteResponse"]["result"][0]["regularMarketPrice"]
        except:
            pass

    # ▼ GOLD（不安定）
    gold_data = safe_request(
        "https://query1.finance.yahoo.com/v7/finance/quote?symbols=GC=F"
    )

    if gold_data and gold_data.get("quoteResponse", {}).get("result"):
        try:
            price_dict["GOLD"] = gold_data["quoteResponse"]["result"][0]["regularMarketPrice"]
        except:
            pass

    # ▼ S3保存（成功したものだけ）
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
        'body': json.dumps(price_dict)
    }