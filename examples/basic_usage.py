import pandas as pd
import numpy as np
from cryptosignalbot import SignalGenerator, MarketAnalyzer

# Генерация тестовых данных
dates = pd.date_range('2024-01-01', periods=100, freq='h')
np.random.seed(42)

close = 50000 + np.cumsum(np.random.randn(100) * 100)
high = close + np.abs(np.random.randn(100) * 50)
low = close - np.abs(np.random.randn(100) * 50)

# Исправление: сначала создаем Series, потом сдвигаем
close_series = pd.Series(close, index=dates)
open_price = close_series.shift(1).fillna(close_series.iloc[0])

data = pd.DataFrame({
    'open': open_price,
    'high': high,
    'low': low,
    'close': close
}, index=dates)

# Запуск бота
sg = SignalGenerator()
ma = MarketAnalyzer()

print("=" * 50)
print("🚀 CryptoSignalBot Test Run")
print("=" * 50)

signal = sg.generate_combined_signal(data)
print(f"\n📊 Combined Signal: {signal['signal']}")
print(f" Confidence: {signal['confidence']}%")
print(f"📝 Summary: {signal['summary']}")

summary = ma.get_market_summary(data)
print(f"\n📈 Trend: {summary['trend_analysis']['trend']} ({summary['trend_analysis']['strength']})")
print(f"💡 Recommendation: {summary['recommendation']}")
print("=" * 50)