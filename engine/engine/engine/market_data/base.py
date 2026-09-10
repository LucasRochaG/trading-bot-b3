from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator


@dataclass(frozen=True)
class Tick:
    ticker: str
    price: float
    volume: int
    timestamp: datetime


class MarketDataFeed(ABC):
    @abstractmethod
    def stream_ticks(self) -> Iterator[Tick]:
        raise NotImplementedError
