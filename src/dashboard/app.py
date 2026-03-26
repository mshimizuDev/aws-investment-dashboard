import streamlit as st
import pandas as pd
import boto3
from io import StringIO

BUCKET_NAME = "investment-dashboard-data-shimizu"
FILE_KEY = "crypto/crypto_price.csv"

s3 = boto3.client('s3')

def load_data_from_s3():
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
    data = obj['Body'].read().decode('utf-8')
    return data

st.title("Crypto Dashboard")

csv_data = load_data_from_s3()

df = pd.read_csv(StringIO(csv_data), header=None)
df.columns = ["timestamp", "BTC", "ETH"]

st.line_chart(df[["BTC", "ETH"]])