import pandas as pd
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
