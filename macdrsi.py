import pandas as pd
import numpy as np
import streamlit as st
import ta.trend
import yfinance as yf
from stocksymbol import StockSymbol
from datetime import datetime as dt
import ta


st.markdown('''
            <style>
            h1{
            text-align: center;
            }
            .css-fg4pbf {
            text-align: center;
            }
            </style>
            ''', unsafe_allow_html=True)

# --- STREAMLIT UI ---
st.title('Stock Recommender System ')
indexs = st.selectbox('Available indexes : ', ['SENSEX', 'NIFTY', 'BANKNIFTY'])
st.info('Select any of the available indexes above !')

# --- DOWNLOAD STOCK TICKERS ---
stockApiKey = '9738ebfc-357d-4cc8-8f30-d719b2a36463'
ss = StockSymbol(stockApiKey)
#indexs = 'SENSEX BANKNIFTY NIFTY S5CONS DJI DJUSCL S5UTIL S5HLTH S5INFT MID'
#print(ss.get_index_list())
tickers = ss.get_symbol_list(index=str(indexs), symbols_only=True)

# --- CALCULATE THE SMA ---
def applytechnicals(df):
    df.dropna(inplace=True)
    df['MACD'] = ta.trend.macd_diff(df.Close)
    df['RSI'] = ta.momentum.rsi(df.Close, window=14)
    df['SMA200'] = ta.trend.sma_indicator(df.Close, window=50)
    df.loc[(df.Close > df.SMA200) & (df.RSI < 30), 'RSISignal'] = 'Buy'
    df.loc[(df.MACD > 0) & (df.MACD.shift(1) < 0), 'MACDSignal'] = 'Buy'
    return df

# --- DOWNLOAD DATA AND SET POSITION ---
def stock(sSymbol):
    df = yf.download(str(sSymbol), start=dt.today() - pd.Timedelta(days=600))
    if not df.empty:
        df = applytechnicals(df)
    return df

# --- CHECK FOR CROSSOVER ---
def check():
    for symbl in tickers:
        data = stock(symbl)
        if not data.empty:
            if data['MACDSignal'].iloc[-1] == 'Buy':
                st.write("MACD buying signal for " + symbl)
            if data['RSISignal'].iloc[-1] == 'Buy':
                st.write("RSI and SMA buying signal for " + symbl)

placeholder = st.empty()
if st.button('Show Stocks'):
    placeholder.info('Please wait searching stocks ...')
    check()
    placeholder.empty()