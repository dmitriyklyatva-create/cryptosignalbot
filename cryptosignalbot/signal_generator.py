import pandas as pd
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
