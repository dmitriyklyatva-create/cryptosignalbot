import pytest, pandas as pd, numpy as np
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
