import yfinance as yf
import numpy as np
import ta
import pandas_ta as pta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import datetime as dt

# --- MA CROSSOVER STRATEGY ---
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

# --- DOWNLOAD DATA & CLEAN IT ---
df = yf.download('MSFT', start=dt.today() - pd.Timedelta(days=3000))
df.dropna(inplace=True)

# --- PLOT THE GRAPH & RESULTS ---
print(df.tail(10))
df.to_csv('data.csv')
bt = Backtest(df, SMACross, cash=10000, commission=0.00, exclusive_orders=True)
bt.run()
bt.plot()
print(bt.run())

# --- GENERATE SIGNALS ---
df['MA1'] = pta.ema(df.Close, length=50)
df['MA2'] = pta.ema(df.Close, length=200)
df.dropna(inplace=True)
df['Signal'] = 0.0
df['Signal'] = np.where(df['MA1'] > df['MA2'], 1.0, 0.0)
df['Position'] = df['Signal'].diff()



