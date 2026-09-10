"""
Orchestrator: conecta todas as partes do robô.

Fluxo:
Feed -> Strategy -> Risk Gate -> Execution -> Persistência
"""

import logging
from datetime import datetime, time as dtime

from engine.config import Config
from engine.market_data.base import MarketDataFeed
from engine.strategy.base import Strategy
from engine.risk.risk_gate import RiskGate
from engine.execution.base import Broker
from engine.persistence.db import init_db
from engine.persistence.models import TradeRecord, EquitySnapshot


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("orchestrator")


class Orchestrator:

    def __init__(
        self,
        config: Config,
        feed: MarketDataFeed,
        strategy: Strategy,
        risk_gate: RiskGate,
        broker: Broker,
    ):
        self.config = config
        self.feed = feed
        self.strategy = strategy
        self.risk_gate = risk_gate
        self.broker = broker

        self.last_prices: dict[str, float] = {}

        Session = init_db(config.database_url)
        self.db = Session()

    def _within_market_hours(self) -> bool:
        now = datetime.now().time()

        open_time = dtime.fromisoformat(
            self.config.market_open
        )

        close_time = dtime.fromisoformat(
            self.config.market_close
        )

        return open_time <= now <= close_time

    def _snapshot_equity(self):
        equity = self.broker.get_equity(
            self.last_prices
        )

        self.db.add(
            EquitySnapshot(
                equity=equity,
                cash=self.broker.get_cash(),
            )
        )

        self.db.commit()

        return equity

    def run(self):

        logger.info(
            f"Iniciando em modo '{self.config.mode}' "
            f"| tickers={self.config.tickers}"
        )

        for tick in self.feed.stream_ticks():

            if not self._within_market_hours():
                logger.info(
                    "Fora do horário de pregão — encerrando loop."
                )
                break

            self.last_prices[tick.ticker] = tick.price

            signal = self.strategy.on_tick(tick)

            if signal is None:
                continue

            equity = self._snapshot_equity()

            if not self.risk_gate.check_daily_loss(equity):
                logger.warning(
                    "CIRCUIT BREAKER ACIONADO — "
                    "perda diária no limite."
                )
                continue

            order = self.risk_gate.approve_order(
                signal=signal,
                price=tick.price,
                current_equity=equity,
                open_positions=self.broker.get_positions(),
                cash=self.broker.get_cash(),
            )

            if order is None:
                continue

            fill = self.broker.execute_order(
                order,
                tick.price,
            )

            self.db.add(
                TradeRecord(
                    ticker=fill.ticker,
                    side=fill.side,
                    quantity=fill.quantity,
                    price=fill.price,
                    reason=order.reason,
                )
            )

            self.db.commit()

            logger.info(
                f"ORDEM EXECUTADA: "
                f"{fill.side.upper()} "
                f"{fill.quantity}x "
                f"{fill.ticker} @ "
                f"{fill.price}"
            )
