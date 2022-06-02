import requests
import streamlit as st
from streamlit_lottie import st_lottie
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


fig = None


# ---FUNCTION TO LOAD LOTTIE FILES---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# ---SMA VALUES FUNCTION---
def sma(dataf, period = 50, column='Close'):
    return dataf[column].rolling(window=period).mean()


# ---LOTTIE FILES OBJECTS---
lottie_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_kuhijlvx.json")
lottie_anim1 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_pmyyjcm7.json")


# ---WEBPAGE DESIGN---
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


# ---HEADER SECTION---
c1, c2, c3 = st.columns(3)
with c2:
    st.markdown("<h2 style='text-align: center; font-size:48px; color: #31333f;'>	&#128184; ALGO ALERT !</h2>"
               , unsafe_allow_html=True)
st.write("---")


# ---TOP COLUMN---
l, m, r = st.columns([1, 1, 1])
with l:
    st_lottie(lottie_anim, key="anim", width=270, height=300)
with m:
    st.write("##")
    st.markdown("<h3 style='text-align: left; font-size:32px; color: #31333f;'>Enter a stock ticker : </h3>"
                , unsafe_allow_html=True)
    ticker = st.text_input("")
    st.write("##")

    if st.button(" 👉 GO !") or ticker:

        # ---DOWNLOADING STOCK DATA AND ASSIGNING OHLC VALUES TO GRAPH OBJ---
        df = yf.download(ticker, start="2020-01-01", end='2022-05-18')

        # ---ADDING SMA VALUES COLUMN---
        df['30SMA'] = sma(df, 30)
        df['10SMA'] = sma(df, 10)

        ema_trace = go.Scatter(x=df.index, y=df['30SMA'], mode='lines', name='50SMA', line=dict(color='orange', width=1.5))
        ema_trace1 = go.Scatter(x=df.index, y=df['10SMA'], mode='lines', name='20SMA', line=dict(color='red', width=1.5))

        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                                 open = df['Open'],
                                                 high = df['High'],
                                                 low = df['Low'],
                                                 close = df['Close'])])
        fig.add_trace(ema_trace)
        fig.add_trace(ema_trace1)

        fig.update_layout(height=600, xaxis_rangeslider_visible=False, title=ticker+' STOCK',
                          yaxis_title='PRICE', xaxis_title='DATE')
with r:
    st_lottie(lottie_anim1, key="anim1", width=410, height=310)
st.write("---")


# ---PLOTTING GRAPH---
cl1, cl2, cl3 = st.columns([1, 10, 1])
with cl2:
    if fig != None:
        st.plotly_chart(fig, use_container_width=True)



















