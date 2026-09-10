from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from engine.market_data.base import Tick


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True)
class Signal:
    ticker: str
    side: Side
    confidence: float
    reason: str


class Strategy(ABC):
    @abstractmethod
    def on_tick(self, tick: Tick) -> Optional[Signal]:
        """
        Chamado a cada tick recebido.
        Retorna um Signal se a estratégia decidir agir,
        ou None caso contrário.
        """
        raise NotImplementedError
