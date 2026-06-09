import os

project_files = {
    "README.md": """# CryptoSignalBot
AI Trading Signal Generator

## Install
pip install cryptosignalbot

## Usage
from cryptosignalbot import SignalGenerator
bot = SignalGenerator()
""",
    "setup.py": """from setuptools import setup, find_packages
setup(
    name='cryptosignalbot',
    version='1.0.0',
    author='YourName',
    author_email='your@email.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['pandas', 'numpy', 'requests'],
)
""",
    "requirements.txt": "pandas\nnumpy\nrequests\nmatplotlib\n",
    "src/__init__.py": """from .indicators import TechnicalIndicators
from .signal_generator import SignalGenerator
from .analyzer import MarketAnalyzer
from .telegram_bot import TelegramNotifier
from .backtester import Backtester
__all__ = ['TechnicalIndicators', 'SignalGenerator', 'MarketAnalyzer', 'TelegramNotifier', 'Backtester']
""",
    "src/indicators.py": """import pandas as pd
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
""",
    "src/signal_generator.py": """import pandas as pd
from .indicators import TechnicalIndicators
class SignalGenerator:
    def __init__(self): self.ind = TechnicalIndicators()
    def generate_macd_signal(self, data):
        m = self.ind.calculate_macd(data['close'])
        cur, prev = m['macd'].iloc[-1], m['macd'].iloc[-2]
        cs, ps = m['signal'].iloc[-1], m['signal'].iloc[-2]
        if prev <= ps and cur > cs: return {'signal': 'BUY', 'strength': 'STRONG', 'indicator': 'MACD'}
        if prev >= ps and cur < cs: return {'signal': 'SELL', 'strength': 'STRONG', 'indicator': 'MACD'}
        return {'signal': 'HOLD', 'strength': 'NEUTRAL', 'indicator': 'MACD'}
    def generate_rsi_signal(self, data, os=30, ob=70):
        r = self.ind.calculate_rsi(data['close']).iloc[-1]
        if r < os: return {'signal': 'BUY', 'strength': 'STRONG', 'indicator': 'RSI'}
        if r > ob: return {'signal': 'SELL', 'strength': 'STRONG', 'indicator': 'RSI'}
        return {'signal': 'HOLD', 'strength': 'NEUTRAL', 'indicator': 'RSI'}
    def generate_supertrend_signal(self, data):
        s = self.ind.calculate_supertrend(data['high'], data['low'], data['close'])
        c, p = s['direction'].iloc[-1], s['direction'].iloc[-2]
        if p == -1 and c == 1: return {'signal': 'BUY', 'strength': 'STRONG', 'indicator': 'SUPERTREND'}
        if p == 1 and c == -1: return {'signal': 'SELL', 'strength': 'STRONG', 'indicator': 'SUPERTREND'}
        return {'signal': 'HOLD', 'strength': 'NEUTRAL', 'indicator': 'SUPERTREND'}
    def generate_combined_signal(self, data):
        ms = self.generate_macd_signal(data)
        rs = self.generate_rsi_signal(data)
        ss = self.generate_supertrend_signal(data)
        sigs = [ms, rs, ss]
        b = sum(1 for x in sigs if x['signal']=='BUY')
        sl = sum(1 for x in sigs if x['signal']=='SELL')
        if b >= 2: sig, conf = 'BUY', min(b/3*100, 100)
        elif sl >= 2: sig, conf = 'SELL', min(sl/3*100, 100)
        else: sig, conf = 'HOLD', 50
        return {'signal': sig, 'confidence': round(conf, 2), 'timestamp': pd.Timestamp.now(), 'individual_signals': {'macd': ms, 'rsi': rs, 'supertrend': ss}, 'summary': f'{b} BUY, {sl} SELL'}
""",
    "src/analyzer.py": """import pandas as pd
from .indicators import TechnicalIndicators
class MarketAnalyzer:
    def __init__(self): self.ind = TechnicalIndicators()
    def analyze_trend(self, data):
        e20 = self.ind.calculate_ema(data['close'], 20).iloc[-1]
        e50 = self.ind.calculate_ema(data['close'], 50).iloc[-1]
        p = data['close'].iloc[-1]
        if p > e20 > e50: t, s = 'UPTREND', 'STRONG'
        elif p > e20: t, s = 'UPTREND', 'WEAK'
        elif p < e20 < e50: t, s = 'DOWNTREND', 'STRONG'
        elif p < e20: t, s = 'DOWNTREND', 'WEAK'
        else: t, s = 'SIDEWAYS', 'NEUTRAL'
        return {'trend': t, 'strength': s, 'price': p}
    def get_market_summary(self, data):
        tr = self.analyze_trend(data)
        return {'trend_analysis': tr, 'recommendation': 'Follow trend', 'timestamp': pd.Timestamp.now()}
""",
    "src/telegram_bot.py": """import requests
class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token; self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
    def send_signal(self, data):
        msg = f"Signal: {data['signal']}\\nConf: {data['confidence']}%"
        try: requests.post(self.url, json={'chat_id': self.chat_id, 'text': msg}); return True
        except: return False
""",
    "src/backtester.py": """import pandas as pd
from .signal_generator import SignalGenerator
class Backtester:
    def __init__(self, symbol='BTC/USDT', capital=10000):
        self.symbol = symbol; self.capital = capital; self.gen = SignalGenerator()
    def run_strategy(self, data, strategy='combined'):
        if len(data) < 50: raise ValueError("Need 50+ candles")
        cap = self.capital; pos = 0; entry = 0; trades = []
        for i in range(50, len(data)):
            w = data.iloc[:i]
            sig = self.gen.generate_combined_signal(w) if strategy=='combined' else self.gen.generate_macd_signal(w)
            price = data['close'].iloc[i]
            if sig['signal']=='BUY' and pos==0: pos=1; entry=price
            elif sig['signal']=='SELL' and pos==1:
                prof = (price-entry)/entry*100; cap *= (1+prof/100)
                trades.append(prof); pos=0
        ret = ((cap-self.capital)/self.capital)*100
        wr = (sum(1 for t in trades if t>0)/len(trades)*100) if trades else 0
        return {'symbol': self.symbol, 'strategy': strategy, 'total_trades': len(trades), 'win_rate': round(wr,2), 'total_return': round(ret,2), 'final_capital': round(cap,2)}
""",
    "examples/basic_usage.py": """import pandas as pd, numpy as np
from cryptosignalbot import SignalGenerator, MarketAnalyzer
dates = pd.date_range('2024-01-01', periods=100, freq='H')
np.random.seed(42)
close = 50000 + np.cumsum(np.random.randn(100)*100)
high = close + np.abs(np.random.randn(100)*50)
low = close - np.abs(np.random.randn(100)*50)
data = pd.DataFrame({'open': close.shift(1).fillna(close.iloc[0]), 'high': high, 'low': low, 'close': close}, index=dates)
sg = SignalGenerator(); ma = MarketAnalyzer()
print(sg.generate_combined_signal(data))
print(ma.get_market_summary(data))
""",
    "examples/advanced_strategy.py": """import pandas as pd, numpy as np
from cryptosignalbot import Backtester
dates = pd.date_range('2023-01-01', periods=500, freq='H')
np.random.seed(123)
close = 45000 + np.cumsum(np.random.randn(500)*200)
high = close + np.abs(np.random.randn(500)*150)
low = close - np.abs(np.random.randn(500)*150)
data = pd.DataFrame({'open': close.shift(1).fillna(close.iloc[0]), 'high': high, 'low': low, 'close': close}, index=dates)
bt = Backtester(symbol='BTC/USDT', capital=10000)
print(bt.run_strategy(data, strategy='combined'))
""",
    "tests/test_indicators.py": """import pytest, pandas as pd, numpy as np
from src.indicators import TechnicalIndicators
@pytest.fixture
def data():
    dates = pd.date_range('2024-01-01', periods=100, freq='H')
    np.random.seed(42)
    c = 50000 + np.cumsum(np.random.randn(100)*100)
    h = c + np.abs(np.random.randn(100)*50)
    l = c - np.abs(np.random.randn(100)*50)
    return pd.DataFrame({'high': h, 'low': l, 'close': c}, index=dates)
def test_rsi(data):
    assert len(TechnicalIndicators().calculate_rsi(data['close'])) == 100
""",
    "docs/tutorial.md": "# Tutorial\nInstall: pip install cryptosignalbot\nSee examples folder for usage."
}

for path, content in project_files.items():
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: {path}")
print("\nDONE! All files created.")