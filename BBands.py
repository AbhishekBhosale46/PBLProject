from backtesting import Strategy
from backtesting import Backtest
import pandas_ta as ta
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import streamlit as st


# --- FUNCTION TO DOWNLOAD THE DATA AND CLEAN IT ---
def downloaddf(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df = df[df.High != df.Low]
    df.reset_index(inplace=True)
    df['EMA'] = ta.sma(df.Close, length=200)
    df['RSI'] = ta.rsi(df.Close, length=2)
    bBands = ta.bbands(df.Close, length=20, std=2.5)
    df = df.join(bBands)
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return df
#data = downloaddf('MSFT', '2018-01-01', '2022-01-01')


# --- CHECK IF UPTREND OR DOWNTREND ---
def addemasignal(df, backCandles):
    emasignal = [0]*len(df)
    for row in range(backCandles, len(df)):
        uptrnd = 1
        dntrnd = 1
        for i in range(row-backCandles, row+1):
            if df.High[i] >= df.EMA[i]:
                dntrnd = 0
            if df.Low[i] <= df.EMA[i]:
                uptrnd = 0
        if uptrnd == 1 and dntrnd == 1:
            emasignal[row] = 3
        elif uptrnd == 1:
            emasignal[row] = 2
        elif dntrnd == 1:
            emasignal[row] = 1
        df['EMASignal'] = emasignal
#addemasignal(data, 6)


# --- ADD ORDER DETAILS ---
def addorderlimit(df, percent):
    orderSignal = [0]*len(df)
    sig = [0]*len(df)
    for i in range(1, len(df)):
        if df.EMASignal[i] == 2 and df.Close[i] <= df['BBL_20_2.5'][i]:
            orderSignal[i] = df.Close[i]-df.Close[i]*percent
            sig[i] = 1
        elif df.EMASignal[i] == 1 and df.Close[i] >= df['BBU_20_2.5'][i]:
            orderSignal[i] = df.Close[i]+df.Close[i]*percent
            sig[i] = -1
    df['OrderSignal'] = orderSignal
    df['Position'] = sig
#addorderlimit(data, 0.00)


# --- PLOTTING BUY SIGNALS ON CHART ---
def pointposbreak(x):
    if x['OrderSignal'] != 0:
        return x['OrderSignal']
    else:
        return np.nan
# data['PointPosBreak'] = data.apply(lambda row: pointposbreak(row), axis=1)
# fig = go.Figure(data=[go.Candlestick(x = data.index,
#                                      open = data['Open'],
#                                      high = data['High'],
#                                      low = data['Low'],
#                                      close = data['Close']),
#                       go.Scatter(x = data.index, y = data.EMA, line=dict(color='orange', width=2), name="EMA"),
#                       go.Scatter(x = data.index, y = data['BBL_20_2.5'], line=dict(color='blue', width=1), name="BBL_20_2.5"),
#                       go.Scatter(x = data.index, y = data['BBU_20_2.5'], line=dict(color='blue', width=1), name="BBU_20_2.5")])
# fig.add_scatter(x = data.index, y = data['PointPosBreak'], mode="markers", marker=dict(size=5, color="MediumPurple"),
#                 name="Signal")


# --- RETURNS THE ORDER SIGNAL ---
# def SIGNAL():
#     return data.OrderSignal


# --- CREATING THE STRATEGY ---
# class MyStrat(Strategy):
#
#     initsize = 0.99
#     ordertime = []
#
#     def init(self):
#         super().init()
#         self.signal = self.I(SIGNAL)
#
#     def next(self):
#         super().next()
#         for j in range(0, len(self.orders)):
#             if self.data.index[-1]-self.ordertime[0] > 5:
#                 self.orders[0].cancel()
#                 self.ordertime.pop(0)
#         if len(self.trades) > 0:
#             if self.data.index[-1]-self.trades[-1].entry_time >= 10:
#                 self.trades[-1].close()
#             if self.trades[-1].is_long and self.data.RSI[-1] >= 50:
#                 self.trades[-1].close()
#             elif self.trades[-1].is_short and self.data.RSI[-1] <= 50:
#                 self.trades[-1].close()
#         if self.signal != 0 and len(self.trades) == 0 and self.data.EMASignal == 2:
#             #Cancel previous orders
#             for j in range(0, len(self.orders)):
#                 self.orders[0].cancel()
#                 self.ordertime.pop(0)
#             #Add new replacement order
#             self.buy(sl = self.signal/2, limit = self.signal, size = self.initsize)
#             self.ordertime.append(self.data.index[-1])
#         elif self.signal != 0 and len(self.trades) == 0 and self.data.EMASignal == 1:
#             #Cancel previous orders
#             for j in range(0, len(self.orders)):
#                 self.orders[0].cancel()
#                 self.ordertime.pop(0)
#             #Add new replacement order
#             self.sell(sl = self.signal*2, limit = self.signal, size = self.initsize)
#             self.ordertime.append(self.data.index[-1])
#
# bt = Backtest(data, MyStrat, cash = 10000, margin = 1/10, commission = .00)
# stat = bt.run()
# print(stat)


