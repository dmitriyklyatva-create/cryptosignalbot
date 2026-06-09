import pandas as pd
import numpy as np
class TechnicalIndicators:
    @staticmethod
    def calculate_ema(data, period=20): return data.ewm(span=period, adjust=False).mean()
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        e1 = data.ewm(span=fast, adjust=False).mean()
        e2 = data.ewm(span=slow, adjust=False).mean()
        m = e1 - e2
        s = m.ewm(span=signal, adjust=False).mean()
        return {'macd': m, 'signal': s, 'histogram': m - s}
    @staticmethod
    def calculate_rsi(data, period=14):
        d = data.diff()
        g = d.where(d > 0, 0).rolling(window=period).mean()
        l = (-d.where(d < 0, 0)).rolling(window=period).mean()
        rs = g / l
        return 100 - (100 / (1 + rs))
    @staticmethod
    def calculate_supertrend(high, low, close, period=10, mult=3.0):
        tr = pd.concat([high-low, abs(high-close.shift()), abs(low-close.shift())], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        hl2 = (high + low) / 2
        up = hl2 + mult * atr
        dn = hl2 - mult * atr
        st = pd.Series(index=close.index, dtype=float)
        dir_ = pd.Series(index=close.index, dtype=int)
        st.iloc[0] = dn.iloc[0]; dir_.iloc[0] = 1
        for i in range(1, len(close)):
            if close.iloc[i] > st.iloc[i-1]: dir_.iloc[i] = 1
            elif close.iloc[i] < st.iloc[i-1]: dir_.iloc[i] = -1
            else: dir_.iloc[i] = dir_.iloc[i-1]
            st.iloc[i] = max(dn.iloc[i], st.iloc[i-1]) if dir_.iloc[i]==1 else min(up.iloc[i], st.iloc[i-1])
        return {'supertrend': st, 'direction': dir_}
