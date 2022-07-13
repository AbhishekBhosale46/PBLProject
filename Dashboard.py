import streamlit as st
import yfinance as yf
import pandas as pd

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
            h1{
            text-align: center;
            font-weight: 600;
            font-size: 2.4rem;
            margin-top: -70px;
            }
            h3{
            text-align: center;
            margin-bottom: 10px;
            margin-top: -15px;
            }
            ''', unsafe_allow_html=True)

st.title(' 📈 ALGO ALERT 📉 ')
st.write('---')
st.subheader('Interactive Dashboard')
tickers = ['TSLA', 'MSFT', 'AAPL', 'BTC-USD', 'ETH-USD', 'RELIANCE.NS']
dropdown = st.multiselect('Pick your assets', tickers)

start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
end = st.date_input('End')
st.write('---')

def relativeret(dataf):
    rel = dataf.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret


if len(dropdown) > 0:
    #df = yf.download(dropdown, start, end)['Adj Close']
    df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
    st.subheader('Returns of the assets'. format(dropdown))
    st.line_chart(df)
