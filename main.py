import requests
import streamlit as st
from streamlit_lottie import st_lottie
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
#import MovingAverage as mova
from backtesting import Strategy
from backtesting import Backtest
import numpy as np
import ta
import pandas_ta as pta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import datetime as dt


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
st.markdown("""
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
        """, unsafe_allow_html=True)    # Remove whitespace from the top of the page and sidebar


# --- HEADER SECTION ---
c1, c2, c3 = st.columns(3)
with c2:
    st.markdown("<h2 style='text-align: center; font-size:48px; color: #31333f;'>	&#128184; ALGO ALERT !</h2>"
               , unsafe_allow_html=True)
st.write("---")


# --- TOP COLUMN ---
l, m, r = st.columns([1, 1, 1])
with l:
    st_lottie(lottie_anim, key="anim", width=270, height=300)
with m:
    st.write("##")
    st.markdown('''<h3 style='text-align: left; font-size:32px; color: #31333f;'>
                    Enter a stock ticker : 
                    </h3>''', unsafe_allow_html=True)
    ticker = st.text_input("")
    st.write("##")
    gobtn = st.button(" 👉 GO !")
with r:
    st_lottie(lottie_anim1, key="anim1", width=410, height=310)


# --- MA Strategy ---
df = yf.download(ticker, start=dt.today() - pd.Timedelta(days=3000))
df = df[df['Volume'] != 0]
df.isna().sum()

df["EMA"] = pta.ema(df.Close, length=100)
df['ATR'] = pta.atr(high=df.High, low=df.Low, close=df.Close, length=14)

def EMASig(df1, l, backcandles):
    sigup=2
    sigdn=1
    for i in range(l-backcandles, l+1):
        if df1.Low[i]<=df1.EMA[i]:
            sigup = 0
        if df1.High[i]>=df1.EMA[i]:
            sigdn = 0
    if sigup:
        return sigup
    elif sigdn:
        return sigdn
    else:
        return 0

dfpl = df[100:1000]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                     open=dfpl['Open'],
                                     high=dfpl['High'],
                                     low=dfpl['Low'],
                                     close=dfpl['Close']),
                      go.Scatter(x=dfpl.index, y=dfpl.EMA, line=dict(color='orange', width=1), name="EMA")])

EMABackCandles = 20
EMASignal = [0] * len(df)
for row in range(EMABackCandles, len(df)):
    EMASignal[row] = EMASig(df, row, EMABackCandles)
df['EMASignal'] = EMASignal
df.dropna(inplace=True)

HLBackCandles = 8
df['mins'] = df['Low'].rolling(window=HLBackCandles).min()
df['maxs'] = df['High'].rolling(window=HLBackCandles).max()
def HLSig(x):
    if x.EMASignal == 1 and x.High >= float(int(x.maxs)):
        return 1
    if x.EMASignal == 2 and x.Low <= x.mins:
        return 2
    else:
        return 0
df["HLSignal"] = df.apply(HLSig, axis=1)
df[df['HLSignal'] == 1]

def pointpos(x):
    if x['HLSignal'] == 1:
        return x['High']+1e-3
    elif x['HLSignal'] == 2:
        return x['Low']-1e-3
    else:
        return np.nan
df['pointpos'] = df.apply(lambda r: pointpos(r), axis=1)

def SIGNAL():
    return df.HLSignal

class MyStrat(Strategy):
    atr_f = 1.
    SLTPR = 1.5
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        if self.signal1==2:
            #sl1 = self.data.Close[-1] - 750e-4 #EURUSD
            #tp1 = self.data.Close[-1] + 600e-4
            #sl1 = self.data.Close[-1] - 30 #ETHUSD
            #tp1 = self.data.Close[-1] + 40
            sl1 = self.data.Close[-1] - self.data.ATR[-1]/self.atr_f #USDCHF
            tp1 = self.data.Close[-1] + self.data.ATR[-1]*self.SLTPR/self.atr_f
            self.buy(sl=sl1, tp=tp1)
        elif self.signal1==1:
            #sl1 = self.data.Close[-1] + 750e-4 #EURUSD
            #tp1 = self.data.Close[-1] - 600e-4
            #sl1 = self.data.Close[-1] + 30 #ETHUSD
            #tp1 = self.data.Close[-1] - 40
            sl1 = self.data.Close[-1] + self.data.ATR[-1]/self.atr_f #USDCHF
            tp1 = self.data.Close[-1] - self.data.ATR[-1]*self.SLTPR/self.atr_f
            self.sell(sl=sl1, tp=tp1)

def showma():
    bt = Backtest(df, MyStrat, cash=10000, commission=0.000)
    stat = bt.run()
    st.write('Strategy Returns [%] : ' + str(dict(stat)['Return [%]']))
    st.write('Buy & Hold Return [%] : ' + str(dict(stat)['Buy & Hold Return [%]']))
    st.write('Win Rate [%] : ' + str(dict(stat)['Win Rate [%]']))


if gobtn or ticker:
    st.header("MA Strategy")
    showma()


st.write("---")




















