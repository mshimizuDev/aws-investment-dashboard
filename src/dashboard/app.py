import streamlit as st
import pandas as pd
import boto3
from io import StringIO

BUCKET_NAME = "investment-dashboard-data-shimizu"

s3 = boto3.client('s3')

def load_data_from_s3(symbol):
    key = f"{symbol}/data.csv"
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    data = obj['Body'].read().decode('utf-8')
    return data

st.title("Crypto Dashboard")

symbol = st.selectbox(
    "Select Asset",
    ["BTC", "ETH"]
)

csv_data = load_data_from_s3(symbol)

df = pd.read_csv(StringIO(csv_data), header=None)
df.columns = ["timestamp", "price"]

st.line_chart(df["price"])

