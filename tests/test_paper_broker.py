from engine.execution.paper_broker import PaperBroker
from engine.risk.risk_gate import Order
from engine.strategy.base import Side


def test_buy_reduces_cash_and_creates_position():
    broker = PaperBroker(initial_cash=10000)

    order = Order(
        ticker="PETR4",
        side=Side.BUY,
        quantity=10,
        reason="test",
    )

    fill = broker.execute_order(
        order,
        current_price=30.0,
    )

    assert fill.ticker == "PETR4"
    assert fill.side == "buy"
    assert fill.quantity == 10
    assert fill.price == 30.0

    assert broker.get_cash() == 9700
    assert broker.get_positions() == {"PETR4": 10}


def test_sell_increases_cash_and_removes_position():
    broker = PaperBroker(initial_cash=10000)

    buy_order = Order(
        ticker="PETR4",
        side=Side.BUY,
        quantity=10,
        reason="test",
    )

    broker.execute_order(
        buy_order,
        current_price=30.0,
    )

    sell_order = Order(
        ticker="PETR4",
        side=Side.SELL,
        quantity=10,
        reason="test",
    )

    fill = broker.execute_order(
        sell_order,
        current_price=35.0,
    )

    assert fill.side == "sell"
    assert broker.get_cash() == 10050
    assert broker.get_positions() == {}


def test_equity_includes_position_value():
    broker = PaperBroker(initial_cash=10000)

    order = Order(
        ticker="VALE3",
        side=Side.BUY,
        quantity=10,
        reason="test",
    )

    broker.execute_order(
        order,
        current_price=50.0,
    )

    equity = broker.get_equity(
        {"VALE3": 55.0}
    )

    assert equity == 10050
