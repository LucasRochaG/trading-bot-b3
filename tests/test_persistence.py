from engine.persistence.db import init_db
from engine.persistence.models import TradeRecord, EquitySnapshot


def test_database_creates_tables(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"

    Session = init_db(database_url)
    session = Session()

    trade = TradeRecord(
        ticker="PETR4",
        side="buy",
        quantity=10,
        price=30.0,
        reason="teste",
    )

    snapshot = EquitySnapshot(
        equity=10000.0,
        cash=9700.0,
    )

    session.add(trade)
    session.add(snapshot)
    session.commit()

    saved_trade = session.query(TradeRecord).first()
    saved_snapshot = session.query(EquitySnapshot).first()

    assert saved_trade is not None
    assert saved_trade.ticker == "PETR4"
    assert saved_trade.quantity == 10
    assert saved_trade.price == 30.0

    assert saved_snapshot is not None
    assert saved_snapshot.equity == 10000.0
    assert saved_snapshot.cash == 9700.0

    session.close()
