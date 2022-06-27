import backtesting
import pandas_ta as ta
import pandas as pd
import yfinance as yf

# --- DOWNLOAD THE DATA ---
data = yf.download('MSFT', start='2018-01-01', end='2022-01-01')
data = data[data.High != data.Low]
data.reset_index(inplace=True)

# --- CALCULATE TECHNICAL INDICATOR VALUES ---
data['SMA'] = ta.sma(data.Close, length=200)
data['RSI'] = ta.rsi(data.Close, length=2)
bBands = ta.bbands(data.Close, length=20, std=2)
data = data.join(bBands)
data.dropna(inplace=True)
data.reset_index(inplace=True)
print(data.tail())

# --- CHECK IF UPTREND OR DOWNTREND ---
