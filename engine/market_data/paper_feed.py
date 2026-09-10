"""
Feed de dados simulado: gera ticks com um random walk, pra testar o
sistema de ponta a ponta sem depender de provedor externo ainda.

Quando for plugar dados reais, criar aqui um `b3_websocket_feed.py`
que implementa a mesma interface MarketDataFeed — o resto do sistema
não muda uma linha.
"""

import random
import time
from datetime import datetime
from typing import Iterator, List

from engine.market_data.base import MarketDataFeed, Tick


class PaperMarketDataFeed(MarketDataFeed):
    def __init__(
        self,
        tickers: List[str],
        tick_interval_sec: float = 1.0,
        base_prices: dict | None = None
    ):
        self.tickers = tickers
        self.tick_interval_sec = tick_interval_sec
        self.prices = base_prices or {
            t: round(random.uniform(15, 120), 2)
            for t in tickers
        }

    def stream_ticks(self) -> Iterator[Tick]:
        while True:
            for ticker in self.tickers:
                change_pct = random.uniform(-0.003, 0.003)

                self.prices[ticker] = round(
                    self.prices[ticker] * (1 + change_pct),
                    2
                )

                yield Tick(
                    ticker=ticker,
                    price=self.prices[ticker],
                    volume=random.randint(100, 5000),
                    timestamp=datetime.now(),
                )

            time.sleep(self.tick_interval_sec)
