import streamlit as st
import pandas as pd

st.title("My Investment Dashboard")

df = pd.read_csv("../data/crypto_price.csv", header=None)

df.columns = ["timestamp","btc","eth"]

btc_latest = df["btc"].iloc[-1]
eth_latest = df["eth"].iloc[-1]

st.metric("BTC Price", btc_latest)
st.metric("ETH Price", eth_latest)

st.line_chart(df[["btc","eth"]])