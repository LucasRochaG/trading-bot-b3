"""
Ponto de entrada do robô.

O MVP funciona somente em modo PAPER.
Nenhuma ordem real será enviada para uma corretora.
"""

from engine.config import config
from engine.market_data.paper_feed import PaperMarketDataFeed
from engine.strategy.moving_average import MovingAverageCrossStrategy
from engine.risk.risk_gate import RiskGate
from engine.execution.paper_broker import PaperBroker
from engine.orchestrator import Orchestrator


def main():

    if config.is_live():
        raise NotImplementedError(
            "Modo 'live' requer implementar um Broker real "
            "em engine/execution/. "
            "Este MVP funciona somente em modo paper."
        )

    feed = PaperMarketDataFeed(
        tickers=config.tickers,
        tick_interval_sec=1.0,
    )

    strategy = MovingAverageCrossStrategy(
        fast_window=config.sma_fast,
        slow_window=config.sma_slow,
    )

    risk_gate = RiskGate(
        initial_capital=config.initial_capital,
        max_position_pct=config.max_position_pct,
        max_daily_loss_pct=config.max_daily_loss_pct,
        max_open_positions=config.max_open_positions,
    )

    broker = PaperBroker(
        initial_cash=config.initial_capital
    )

    orchestrator = Orchestrator(
        config=config,
        feed=feed,
        strategy=strategy,
        risk_gate=risk_gate,
        broker=broker,
    )

    orchestrator.run()


if __name__ == "__main__":
    main()
