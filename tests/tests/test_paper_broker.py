from engine.execution.paper_broker import PaperBroker
from engine.risk.risk_gate import Order
from engine.strategy.base import Side


def test_buy_reduces_cash_and_creates_position():
    broker = PaperBroker(initial_cash=10000)

    order = Order(
        ticker="PETR4",
        side=Side.BUY,
        quantity=100,
        reason="teste compra",
    )

    fill = broker.execute_order(
        order,
        current_price=30.0,
    )

    assert fill.ticker == "PETR4"
    assert fill.side == "buy"
    assert fill.quantity == 100
    assert fill.price == 30.0

    assert broker.get_cash() == 7000
    assert broker.get_positions() == {"PETR4": 100}


def test_sell_returns_cash_and_closes_position():
    broker = PaperBroker(initial_cash=10000)

    buy_order = Order(
        ticker="PETR4",
        side=Side.BUY,
        quantity=100,
        reason="teste compra",
    )

    broker.execute_order(
        buy_order,
        current_price=30.0,
    )

    sell_order = Order(
        ticker="PETR4",
        side=Side.SELL,
        quantity=100,
        reason="teste venda",
    )

    fill = broker.execute_order(
        sell_order,
        current_price=35.0,
    )

    assert fill.side == "sell"
    assert fill.quantity == 100
    assert fill.price == 35.0

    assert broker.get_cash() == 10500
    assert broker.get_positions() == {}


def test_equity_includes_position_value():
    broker = PaperBroker(initial_cash=10000)

    order = Order(
        ticker="VALE3",
        side=Side.BUY,
        quantity=100,
        reason="teste",
    )

    broker.execute_order(
        order,
        current_price=50.0,
    )

    equity = broker.get_equity(
        {
            "VALE3": 60.0,
        }
    )

    assert equity == 11000
