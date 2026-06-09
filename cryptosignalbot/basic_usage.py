import pandas as pd
import numpy as np
from cryptosignalbot import SignalGenerator, MarketAnalyzer


def generate_sample_data():
    dates = pd.date_range('2024-01-01', periods=100, freq='H')
    
    np.random.seed(42)
    close = 50000 + np.cumsum(np.random.randn(100) * 100)
    
    high = close + np.abs(np.random.randn(100) * 50)
    low = close - np.abs(np.random.randn(100) * 50)
    open_price = close.shift(1).fillna(close.iloc[0])
    volume = np.random.randint(1000, 10000, 100)
    
    data = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }, index=dates)
    
    return data


def main():
    print("=" * 60)
    print("🚀 CryptoSignalBot - Basic Usage Example")
    print("=" * 60)
    
    print("\n📊 Generating sample market data...")
    data = generate_sample_data()
    print(f"✓ Generated {len(data)} candles")
    
    signal_gen = SignalGenerator()
    analyzer = MarketAnalyzer()
    
    print("\n🎯 Generating trading signals...")
    macd_signal = signal_gen.generate_macd_signal(data)
    rsi_signal = signal_gen.generate_rsi_signal(data)
    supertrend_signal = signal_gen.generate_supertrend_signal(data)
    combined_signal = signal_gen.generate_combined_signal(data)
    
    print(f"\n📈 MACD Signal: {macd_signal['signal']} ({macd_signal['strength']})")
    print(f"   Details: {macd_signal['details']}")
    
    print(f"\n📊 RSI Signal: {rsi_signal['signal']} ({rsi_signal['strength']})")
    print(f"   Details: {rsi_signal['details']}")
    
    print(f"\n🔄 Supertrend Signal: {supertrend_signal['signal']} ({supertrend_signal['strength']})")
    print(f"   Details: {supertrend_signal['details']}")
    
    print(f"\n🎯 COMBINED SIGNAL: {combined_signal['signal']}")
    print(f"   Confidence: {combined_signal['confidence']}%")
    print(f"   Summary: {combined_signal['summary']}")
    
    print("\n🔍 Market Analysis:")
    summary = analyzer.get_market_summary(data)
    print(f"   Trend: {summary['trend_analysis']['trend']} ({summary['trend_analysis']['strength']})")
    print(f"   Volatility: {summary['volatility_analysis']['volatility']}")
    print(f"   Recommendation: {summary['recommendation']}")
    
    print("\n" + "=" * 60)
    print("✅ Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()