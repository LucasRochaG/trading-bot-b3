"""
Configuração central do robô.
Tudo que muda entre paper/real, ou entre ambientes, vem de env vars —
nunca hardcoded, pra não vazar credenciais no repo.
"""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    mode: str = os.getenv("TRADING_MODE", "paper")

    tickers: List[str] = field(
        default_factory=lambda: os.getenv(
            "TICKERS",
            "PETR4,VALE3,ITUB4,BBDC4,WEGE3"
        ).split(",")
    )

    market_open: str = os.getenv("MARKET_OPEN", "10:00")
    market_close: str = os.getenv("MARKET_CLOSE", "17:00")
    timezone: str = "America/Sao_Paulo"

    initial_capital: float = float(
        os.getenv("INITIAL_CAPITAL", "10000.0")
    )

    max_position_pct: float = float(
        os.getenv("MAX_POSITION_PCT", "0.10")
    )

    max_daily_loss_pct: float = float(
        os.getenv("MAX_DAILY_LOSS_PCT", "0.03")
    )

    max_open_positions: int = int(
        os.getenv("MAX_OPEN_POSITIONS", "5")
    )

    sma_fast: int = int(os.getenv("SMA_FAST", "9"))
    sma_slow: int = int(os.getenv("SMA_SLOW", "21"))

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///trading_bot.db"
    )

    broker_api_key: str = os.getenv("BROKER_API_KEY", "")
    broker_api_secret: str = os.getenv("BROKER_API_SECRET", "")

    def is_live(self) -> bool:
        return self.mode == "live"


config = Config()
