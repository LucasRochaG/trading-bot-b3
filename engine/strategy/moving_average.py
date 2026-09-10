"""
Estratégia de exemplo — NÃO é recomendação de investimento.
É apenas um placeholder funcional para validar o robô de ponta a ponta.

Lógica:
- média móvel rápida cruza acima da lenta → COMPRA
- média móvel rápida cruza abaixo da lenta → VENDA
"""

from collections import defaultdict, deque
from typing import Optional

from engine.market_data.base import Tick
from engine.strategy.base import Strategy, Signal, Side


class MovingAverageCrossStrategy(Strategy):
    def __init__(self, fast_window: int = 9, slow_window: int = 21):
        self.fast_window = fast_window
        self.slow_window = slow_window

        self.history: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=slow_window)
        )

        self.last_state: dict[str, str] = {}

    def _sma(
        self,
        prices: deque,
        window: int
    ) -> Optional[float]:

        if len(prices) < window:
            return None

        return sum(list(prices)[-window:]) / window

    def on_tick(
        self,
        tick: Tick
    ) -> Optional[Signal]:

        hist = self.history[tick.ticker]
        hist.append(tick.price)

        fast = self._sma(hist, self.fast_window)
        slow = self._sma(hist, self.slow_window)

        if fast is None or slow is None:
            return None

        current_state = "above" if fast > slow else "below"

        previous_state = self.last_state.get(tick.ticker)

        self.last_state[tick.ticker] = current_state

        if previous_state is None or previous_state == current_state:
            return None

        if current_state == "above":
            return Signal(
                tick.ticker,
                Side.BUY,
                confidence=0.6,
                reason=(
                    f"SMA{self.fast_window} cruzou acima "
                    f"da SMA{self.slow_window}"
                ),
            )

        return Signal(
            tick.ticker,
            Side.SELL,
            confidence=0.6,
            reason=(
                f"SMA{self.fast_window} cruzou abaixo "
                f"da SMA{self.slow_window}"
            ),
        )
