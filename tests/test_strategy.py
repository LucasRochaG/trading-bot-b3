from datetime import datetime

from engine.market_data.base import Tick
from engine.strategy.moving_average import MovingAverageCrossStrategy

def make_tick(ticker, price):
return Tick(
ticker=ticker,
price=price,
volume=100,
timestamp=datetime.now(),
)

def test_no_signal_with_insufficient_history():
strat = MovingAverageCrossStrategy(
fast_window=3,
slow_window=5,
)

```
for price in [10, 10, 10]:
    signal = strat.on_tick(
        make_tick("PETR4", price)
    )

    assert signal is None
```

def test_detects_bullish_crossover():
strat = MovingAverageCrossStrategy(
fast_window=2,
slow_window=4,
)

```
prices = [10, 10, 10, 10, 15, 20]

signals = []

for price in prices:
    signal = strat.on_tick(
        make_tick("PETR4", price)
    )

    if signal is not None:
        signals.append(signal)

assert len(signals) > 0
assert signals[0].side.value == "buy"
```
