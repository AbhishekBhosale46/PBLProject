import requests
import streamlit as st
from streamlit_lottie import st_lottie
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import BBands as bb
from backtesting import Strategy
from backtesting import Backtest
import numpy as np
import ta
import pandas_ta as pta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


fig = None


# --- MA CROSSOVER STRATEGY ---
def macross():

    class SMACross(Strategy):
        n1 = 50
        n2 = 200

        def init(self):
            close = self.data.Close
            self.sma1 = self.I(ta.trend.ema_indicator, pd.Series(close), self.n1)
            self.sma2 = self.I(ta.trend.ema_indicator, pd.Series(close), self.n2)

        def next(self):
            if crossover(self.sma1, self.sma2):
                self.buy()
            elif crossover(self.sma2, self.sma1):
                self.sell()

    df = yf.download(ticker, start=dt.today() - pd.Timedelta(days=3000))
    df.dropna(inplace=True)

    bt = Backtest(df, SMACross, cash=10000, commission=0.00, exclusive_orders=True)
    stat = bt.run()

    df['MA1'] = pta.ema(df.Close, length=50)
    df['MA2'] = pta.ema(df.Close, length=200)
    df.dropna(inplace=True)
    df['Signal'] = 0.0
    df['Signal'] = np.where(df['MA1'] > df['MA2'], 1.0, 0.0)
    df['Position'] = df['Signal'].diff()

    plot = go.Figure(data=[go.Candlestick(x = df.index,
                                          open = df['Open'],
                                          high = df['High'],
                                          low = df['Low'],
                                          close = df['Close']),
                                          go.Scatter(x = df.index, y = df.MA1, line=dict(color='orange', width=1.5), name="EMA1"),
                                          go.Scatter(x = df.index, y = df.MA2, line=dict(color='blue', width=1.5), name="EMA2")])
    plot.update_layout(height=600, xaxis_rangeslider_visible=False, title=ticker+' STOCK', yaxis_title='PRICE', xaxis_title='DATE')

    st.plotly_chart(plot, use_container_width=True)
    st.write('Strategy Returns [%] : ' + str(dict(stat)['Return [%]']))
    st.write('Buy & Hold Return [%] : ' + str(dict(stat)['Buy & Hold Return [%]']))
    st.write('Win Rate [%] : ' + str(dict(stat)['Win Rate [%]']))


# --- FUNCTION TO LOAD LOTTIE FILES ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# --- LOTTIE FILES OBJECTS ---
lottie_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_kuhijlvx.json")
lottie_anim1 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_pmyyjcm7.json")


# --- WEBPAGE DESIGN ---
st.set_page_config(layout="wide")
st.markdown('''
            <style>
            .css-18e3th9 {
            padding-top: 1rem;
            padding-right: 6rem;  
            }
            .css-1d391kg {
            padding-top: 3.5rem;
            padding-left: 0rem;
            padding-right: 0rem;
            }
            </style>
            ''', unsafe_allow_html=True)    # Remove whitespace from the top of the page and sidebar


# --- HEADER SECTION ---
c1, c2, c3 = st.columns(3)
with c2:
    st.markdown('''
                <h2 style='text-align: center; font-size:48px; color: #31333f;'>
                &#128184; ALGO ALERT !
                </h2>''', unsafe_allow_html=True)
st.write("---")


# --- TOP COLUMN ---
l, m, r = st.columns([1, 1, 1])
with l:
    st_lottie(lottie_anim, key="anim", width=270, height=300)
with m:
    st.write("##")
    st.markdown('''
                <h3 style='text-align: left; font-size:32px; color: #31333f;'>
                Enter a stock ticker : 
                </h3>
                ''', unsafe_allow_html=True)
    ticker = st.text_input("")
    st.write("##")
    gobtn = st.button(" 👉 GO !")
with r:
    st_lottie(lottie_anim1, key="anim1", width=410, height=310)

st.write("---")
if gobtn or ticker:
    st.subheader("Moving Average Crossover Strategy")
    macross()


st.write("---")




















