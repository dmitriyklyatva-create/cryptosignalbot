import pandas as pd
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
