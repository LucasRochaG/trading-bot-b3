from engine.risk.risk_gate import RiskGate
from engine.strategy.base import Signal, Side


def make_gate(**overrides):
    defaults = dict(
        initial_capital=10000,
        max_position_pct=0.10,
        max_daily_loss_pct=0.03,
        max_open_positions=5,
    )
    defaults.update(overrides)
    return RiskGate(**defaults)


def test_buy_signal_sized_within_position_limit():
    gate = make_gate()

    signal = Signal(
        "PETR4",
        Side.BUY,
        confidence=0.6,
        reason="test",
    )

    order = gate.approve_order(
        signal,
        price=30.0,
        current_equity=10000,
        open_positions={},
        cash=10000,
    )

    assert order is not None
    assert order.quantity * 30.0 <= 10000 * 0.10 + 30.0


def test_rejects_buy_when_max_positions_reached():
    gate = make_gate(max_open_positions=2)

    signal = Signal(
        "WEGE3",
        Side.BUY,
        confidence=0.6,
        reason="test",
    )

    order = gate.approve_order(
        signal,
        price=40.0,
        current_equity=10000,
        open_positions={
            "PETR4": 10,
            "VALE3": 5,
        },
        cash=5000,
    )

    assert order is None


def test_rejects_sell_without_position():
    gate = make_gate()

    signal = Signal(
        "ITUB4",
        Side.SELL,
        confidence=0.6,
        reason="test",
    )

    order = gate.approve_order(
        signal,
        price=25.0,
        current_equity=10000,
        open_positions={},
        cash=10000,
    )

    assert order is None


def test_circuit_breaker_halts_trading():
    gate = make_gate(max_daily_loss_pct=0.03)

    still_ok = gate.check_daily_loss(
        current_equity=9800
    )

    assert still_ok is True

    still_ok = gate.check_daily_loss(
        current_equity=9600
    )

    assert still_ok is False
    assert gate.trading_halted is True

    signal = Signal(
        "PETR4",
        Side.BUY,
        confidence=0.9,
        reason="test",
    )

    order = gate.approve_order(
        signal,
        price=30.0,
        current_equity=9600,
        open_positions={},
        cash=9600,
    )

    assert order is None


def test_rejects_corrupted_price():
    gate = make_gate()

    signal = Signal(
        "PETR4",
        Side.BUY,
        confidence=0.6,
        reason="test",
    )

    order = gate.approve_order(
        signal,
        price=-5.0,
        current_equity=10000,
        open_positions={},
        cash=10000,
    )

    assert order is None
