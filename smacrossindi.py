import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
from stocksymbol import StockSymbol
from datetime import datetime as dt


st.markdown('''
            <style>
            h1{
            text-align: center;
            }
            .css-fg4pbf {
            text-align: center;
            }
            h1{
            text-align: center;
            font-weight: 600;
            margin-top: -70px;
            }
            h3{
            text-align: center;
            margin-top: -25px;
            margin-bottom: 15px;
            }
            </style>
            ''', unsafe_allow_html=True)

# --- STREAMLIT UI ---
st.title(' 📈 ALGO ALERT 📉 ')
st.write('---')
st.subheader('Stock Recommendation System 2')
indexs = st.selectbox('Available indices : ', ['SENSEX', 'NIFTY', 'BANKNIFTY'])
st.info('Select any of the available indices above !')

# --- DOWNLOAD STOCK TICKERS ---
stockApiKey = '9738ebfc-357d-4cc8-8f30-d719b2a36463'
ss = StockSymbol(stockApiKey)
#indexs = 'SENSEX BANKNIFTY NIFTY'
tickers = ss.get_symbol_list(index=str(indexs), symbols_only=True)

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
        data = stock(symbl).Position
        if len(data) > 1:
            if data[-1] and data.diff()[-1]:
                st.write("Bullish cross over in " + symbl)

placeholder = st.empty()
if st.button('Show Stocks'):
    placeholder.info('Please wait searching stocks ...')
    check()
    placeholder.empty()
