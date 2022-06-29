import requests
import streamlit as st
from streamlit_lottie import st_lottie
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import BBands as bb
from backtesting import Strategy
from backtesting import Backtest


fig = None


# --- BOLLINGER BANDS STRATEGY ---
def bollingerbands():
    stockdata = bb.downloaddf(ticker, '2018-01-01', '2022-01-01')
    bb.addemasignal(stockdata, 6)
    bb.addorderlimit(stockdata, 0.00)
    stockdata['PointPosBreak'] = stockdata.apply(lambda row: bb.pointposbreak(row), axis=1)
    fig = go.Figure(data=[go.Candlestick(x = stockdata.index,
                                         open = stockdata['Open'],
                                         high = stockdata['High'],
                                         low = stockdata['Low'],
                                         close = stockdata['Close']),
                          go.Scatter(x = stockdata.index, y = stockdata.EMA, line=dict(color='orange', width=2), name="EMA"),
                          go.Scatter(x = stockdata.index, y = stockdata['BBL_20_2.5'], line=dict(color='blue', width=1), name="BBL_20_2.5"),
                          go.Scatter(x = stockdata.index, y = stockdata['BBU_20_2.5'], line=dict(color='blue', width=1), name="BBU_20_2.5")])
    fig.add_scatter(x = stockdata.index, y = stockdata['PointPosBreak'], mode="markers", marker=dict(size=5, color="MediumPurple"),
                    name="Signal")
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

    def SIGNAL():
        return stockdata.OrderSignal

    class MyStrat(Strategy):

        initsize = 0.99
        ordertime = []

        def init(self):
            super().init()
            self.signal = self.I(SIGNAL)

        def next(self):
            super().next()
            for j in range(0, len(self.orders)):
                if self.data.index[-1]-self.ordertime[0] > 5:
                    self.orders[0].cancel()
                    self.ordertime.pop(0)
            if len(self.trades) > 0:
                if self.data.index[-1]-self.trades[-1].entry_time >= 10:
                    self.trades[-1].close()
                if self.trades[-1].is_long and self.data.RSI[-1] >= 50:
                    self.trades[-1].close()
                elif self.trades[-1].is_short and self.data.RSI[-1] <= 50:
                    self.trades[-1].close()
            if self.signal != 0 and len(self.trades) == 0 and self.data.EMASignal == 2:
                #Cancel previous orders
                for j in range(0, len(self.orders)):
                    self.orders[0].cancel()
                    self.ordertime.pop(0)
                #Add new replacement order
                self.buy(sl = self.signal/2, limit = self.signal, size = self.initsize)
                self.ordertime.append(self.data.index[-1])
            elif self.signal != 0 and len(self.trades) == 0 and self.data.EMASignal == 1:
                #Cancel previous orders
                for j in range(0, len(self.orders)):
                    self.orders[0].cancel()
                    self.ordertime.pop(0)
                #Add new replacement order
                self.sell(sl = self.signal*2, limit = self.signal, size = self.initsize)
                self.ordertime.append(self.data.index[-1])

    bt = Backtest(stockdata, MyStrat,  cash = 10000, margin = 1/10, commission = .00)
    stat = bt.run()
    st.write('Strategy Returns [%] - ' + str(dict(stat)['Return [%]']))
    st.write('Win Rate [%] - ' + str(dict(stat)['Win Rate [%]']))



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

if gobtn or ticker:
    st.header("Bollinger Bands Strategy")
    bollingerbands()


st.write("---")




















