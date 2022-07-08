import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
from stocksymbol import StockSymbol
from datetime import datetime as dt

st.title('Stock Recommender ')

# --- DOWNLOAD STOCK TICKERS ---
stockApiKey = '9738ebfc-357d-4cc8-8f30-d719b2a36463'
ss = StockSymbol(stockApiKey)
indexs = 'SENSEX BANKNIFTY NIFTY'
tickers = ss.get_symbol_list(index='SENSEX', symbols_only=True)

# --- CALCULATE THE SMA ---
def applytechnicals(df):
    df['SMA50'] = df.Close.rolling(10).mean()
    df['SMA200'] = df.Close.rolling(20).mean()
    df.dropna(inplace=True)
    df = df[['Close','SMA50','SMA200']]
    return df

# --- DOWNLOAD DATA AND SET POSITION ---
def stock(sSymbol):
    df = yf.download(str(sSymbol),start=dt.today() - pd.Timedelta(days=80))
    df = applytechnicals(df)
    df['Position'] = np.where(df['SMA50']>df['SMA200'], 1, 0)
    return df

# --- CHECK FOR CROSSOVER ---
def check():
    for symbl in tickers:
        if len(stock(symbl).Position) > 1:
            if stock(symbl).Position[-1] and stock(symbl).Position.diff()[-1]:
                st.write("Bullish cross over in " + symbl)

if st.button('Show results : '):
    check()
