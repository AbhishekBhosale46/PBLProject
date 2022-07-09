import pandas as pd
import numpy as np
import streamlit as st
import ta.trend
import yfinance as yf
from stocksymbol import StockSymbol
from datetime import datetime as dt
import ta


# --- DOWNLOAD STOCK TICKERS ---
stockApiKey = '9738ebfc-357d-4cc8-8f30-d719b2a36463'
ss = StockSymbol(stockApiKey)
#indexs = 'SENSEX BANKNIFTY NIFTY S5CONS DJI DJUSCL S5UTIL S5HLTH S5INFT MID'
print(ss.get_index_list())
tickers = ss.get_symbol_list(index='S5UTIL', symbols_only=True)

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
                print("MACD buying signal for " + symbl)
            if data['RSISignal'].iloc[-1] == 'Buy':
                print("RSI buying signal for " + symbl)

check()