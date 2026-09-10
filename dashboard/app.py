"""
Dashboard simples do robô.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from engine.persistence.models import (
    TradeRecord,
    EquitySnapshot,
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///data/trading_bot.db",
)

app = Flask(__name__)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/trades")
def api_trades():

    session = Session()

    trades = (
        session.query(TradeRecord)
        .order_by(desc(TradeRecord.timestamp))
        .limit(200)
        .all()
    )

    session.close()

    return jsonify([
        {
            "ticker": trade.ticker,
            "side": trade.side,
            "quantity": trade.quantity,
            "price": trade.price,
            "reason": trade.reason,
            "timestamp": trade.timestamp.isoformat(),
        }
        for trade in trades
    ])


@app.route("/api/equity")
def api_equity():

    session = Session()

    snapshots = (
        session.query(EquitySnapshot)
        .order_by(EquitySnapshot.timestamp)
        .all()
    )

    session.close()

    return jsonify([
        {
            "equity": snapshot.equity,
            "cash": snapshot.cash,
            "timestamp": snapshot.timestamp.isoformat(),
        }
        for snapshot in snapshots
    ])


@app.route("/api/summary")
def api_summary():

    session = Session()

    trades = session.query(TradeRecord).all()

    last_equity = (
        session.query(EquitySnapshot)
        .order_by(desc(EquitySnapshot.timestamp))
        .first()
    )

    session.close()

    buys = [
        trade for trade in trades
        if trade.side == "buy"
    ]

    sells = [
        trade for trade in trades
        if trade.side == "sell"
    ]

    return jsonify({
        "total_trades": len(trades),
        "buys": len(buys),
        "sells": len(sells),
        "current_equity": (
            last_equity.equity
            if last_equity
            else None
        ),
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv("PORT", "5000")
        ),
        debug=False,
    )
