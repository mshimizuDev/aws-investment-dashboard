import streamlit as st
import pandas as pd
import boto3
from io import StringIO

BUCKET_NAME = "investment-dashboard-data-shimizu"

s3 = boto3.client('s3')

# ▼ S3からデータ取得
def load_data(symbol):
    key = f"{symbol}/data.csv"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        data = obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(data), header=None)
        df.columns = ["timestamp", "price"]
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except:
        return None


# ▼ UIタイトル
st.title("📊 Investment Dashboard")

# ▼ 表示したい資産
assets = ["BTC", "ETH", "USDJPY", "SP500", "GOLD"]

data_dict = {}

# ▼ データ読み込み
for asset in assets:
    df = load_data(asset)
    if df is not None:
        data_dict[asset] = df

# -------------------------
# KPI表示（現在価格）
# -------------------------
st.subheader("📌 Current Prices")

cols = st.columns(len(data_dict))

for i, (asset, df) in enumerate(data_dict.items()):
    latest_price = df["price"].iloc[-1]
    cols[i].metric(asset, f"{latest_price:.2f}")

# -------------------------
# グラフ表示（上段）
# -------------------------
st.subheader("📈 Market Charts")

top_assets = ["BTC", "ETH", "USDJPY"]
cols = st.columns(3)

for i, asset in enumerate(top_assets):
    if asset in data_dict:
        df = data_dict[asset]
        with cols[i]:
            st.write(asset)
            st.line_chart(df.set_index("timestamp")["price"])

# -------------------------
# グラフ表示（下段）
# -------------------------
bottom_assets = ["SP500", "GOLD"]
cols = st.columns(2)

for i, asset in enumerate(bottom_assets):
    if asset in data_dict:
        df = data_dict[asset]
        with cols[i]:
            st.write(asset)
            st.line_chart(df.set_index("timestamp")["price"])