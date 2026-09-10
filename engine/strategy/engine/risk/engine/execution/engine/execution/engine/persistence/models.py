from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class TradeRecord(Base):
    """Cada ordem executada (compra ou venda)."""

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    side = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)


class EquitySnapshot(Base):
    """Snapshot do patrimônio total."""

    __tablename__ = "equity_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equity = Column(Float, nullable=False)
    cash = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
