from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from engine.risk.risk_gate import Order


@dataclass(frozen=True)
class Fill:
    ticker: str
    side: str
    quantity: int
    price: float
    timestamp: datetime


class Broker(ABC):
    @abstractmethod
    def execute_order(self, order: Order, current_price: float) -> Fill:
        raise NotImplementedError

    @abstractmethod
    def get_cash(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_positions(self) -> dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    def get_equity(self, current_prices: dict[str, float]) -> float:
        raise NotImplementedError
