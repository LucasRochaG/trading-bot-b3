"""
Risk Gate: todo sinal passa por aqui antes de virar ordem.

Regras:
1. Limite de posição por ativo
2. Limite de posições abertas simultâneas
3. Circuit breaker de perda diária
4. Sanity check de preço
"""

from dataclasses import dataclass

from engine.strategy.base import Signal, Side


@dataclass
class Order:
    ticker: str
    side: Side
    quantity: int
    reason: str


class RiskGate:
    def __init__(
        self,
        initial_capital: float,
        max_position_pct: float,
        max_daily_loss_pct: float,
        max_open_positions: int,
    ):
        self.initial_capital = initial_capital
        self.max_position_pct = max_position_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_open_positions = max_open_positions
        self.trading_halted = False

    def check_daily_loss(self, current_equity: float) -> bool:
        loss_pct = (
            self.initial_capital - current_equity
        ) / self.initial_capital

        if loss_pct >= self.max_daily_loss_pct:
            self.trading_halted = True
            return False

        return True

    def _sanity_check_price(self, price: float) -> bool:
        return 0 < price < 100_000

    def approve_order(
        self,
        signal: Signal,
        price: float,
        current_equity: float,
        open_positions: dict[str, int],
        cash: float,
    ) -> Order | None:

        if self.trading_halted:
            return None

        if not self._sanity_check_price(price):
            return None

        if signal.side == Side.BUY:

            if (
                len(open_positions) >= self.max_open_positions
                and signal.ticker not in open_positions
            ):
                return None

            max_position_value = (
                current_equity * self.max_position_pct
            )

            quantity = int(max_position_value // price)

            if quantity < 1 or quantity * price > cash:
                return None

            return Order(
                signal.ticker,
                Side.BUY,
                quantity,
                signal.reason,
            )

        elif signal.side == Side.SELL:

            held_qty = open_positions.get(signal.ticker, 0)

            if held_qty <= 0:
                return None

            return Order(
                signal.ticker,
                Side.SELL,
                held_qty,
                signal.reason,
            )

        return None
