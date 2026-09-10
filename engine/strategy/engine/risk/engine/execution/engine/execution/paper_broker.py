"""
Broker simulado para o modo PAPER.

As ordens são executadas instantaneamente no preço atual.
O caixa e as posições ficam em memória.
"""

from datetime import datetime

from engine.execution.base import Broker, Fill
from engine.risk.risk_gate import Order


class PaperBroker(Broker):
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.positions: dict[str, int] = {}

    def execute_order(
        self,
        order: Order,
        current_price: float
    ) -> Fill:

        cost = order.quantity * current_price

        if order.side.value == "buy":
            self.cash -= cost

            self.positions[order.ticker] = (
                self.positions.get(order.ticker, 0)
                + order.quantity
            )

        else:
            self.cash += cost

            self.positions[order.ticker] = (
                self.positions.get(order.ticker, 0)
                - order.quantity
            )

            if self.positions[order.ticker] <= 0:
                del self.positions[order.ticker]

        return Fill(
            ticker=order.ticker,
            side=order.side.value,
            quantity=order.quantity,
            price=current_price,
            timestamp=datetime.now(),
        )

    def get_cash(self) -> float:
        return self.cash

    def get_positions(self) -> dict[str, int]:
        return dict(self.positions)

    def get_equity(
        self,
        current_prices: dict[str, float]
    ) -> float:

        positions_value = sum(
            qty * current_prices.get(ticker, 0)
            for ticker, qty in self.positions.items()
        )

        return self.cash + positions_value
