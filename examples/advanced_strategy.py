import pandas as pd, numpy as np
from cryptosignalbot import Backtester
dates = pd.date_range('2023-01-01', periods=500, freq='H')
np.random.seed(123)
close = 45000 + np.cumsum(np.random.randn(500)*200)
high = close + np.abs(np.random.randn(500)*150)
low = close - np.abs(np.random.randn(500)*150)
data = pd.DataFrame({'open': close.shift(1).fillna(close.iloc[0]), 'high': high, 'low': low, 'close': close}, index=dates)
bt = Backtester(symbol='BTC/USDT', capital=10000)
print(bt.run_strategy(data, strategy='combined'))
