import yfinance as yf
import pandas as pd
import pandas_ta as pa
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np
from backtesting import Strategy, Backtest



df = yf.download('MSFT', start='2018-01-01')
df = df[df['Volume'] != 0]
df.isna().sum()
#df.reset_index(drop=True, inplace=True)


df["EMA"] = pa.ema(df.Close, length=100)
df['ATR'] = pa.atr(high=df.High, low=df.Low, close=df.Close, length=14)


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
#fig.show()


EMABackCandles = 20
EMASignal = [0] * len(df)
for row in range(EMABackCandles, len(df)):
    EMASignal[row] = EMASig(df, row, EMABackCandles)
df['EMASignal'] = EMASignal


df.dropna(inplace=True)
#df.reset_index(drop=True, inplace=True)


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


dfpl = df[100:250]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                     open=dfpl['Open'],
                                     high=dfpl['High'],
                                     low=dfpl['Low'],
                                     close=dfpl['Close']),
                                     go.Scatter(x=dfpl.index, y=dfpl.EMA, line=dict(color='orange', width=1), name="EMA")])
fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="Signal")
#fig.show()


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
bt = Backtest(df, MyStrat, cash=10000, commission=.000)
stat = bt.run()
print(stat)


