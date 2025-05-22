from datetime import datetime
import pandas as pd
from myLib.brokers import (
    BrokerAbstractClass,
    OrderType,
    LimitOrderTypedDict,
    MarketOrderTypedDict,
)
from myLib.strategies.withDoubleTrend.types import DoubleTrendSignals


def manage_long(
    broker: BrokerAbstractClass,
    orders: list[LimitOrderTypedDict | MarketOrderTypedDict],
    data: pd.DataFrame,
    positions: dict[str, int],
) -> None:
    """Manage long positions and related orders for DoubleTrend strategy.

    Args:
        broker: Broker instance for order management
        orders: List of current pending orders
        data: Market data containing strategy levels ('ST 10 3 UP' and 'ST 20 5 LOW' columns)
        positions: Dictionary containing position size ('size' key)
    """
    position_size = positions.get("size", 0)

    # Validate position size
    if position_size < 0:
        raise ValueError("Position size cannot be negative.")

    # Check strategy conditions
    condition = pd.notna(data.get("ST 10 3 UP")) and pd.notna(data.get("ST 20 5 LOW"))
    is_close_time = (
        pd.to_datetime(data.get("DATE")).time() == pd.Timestamp("23:40:00").time()
    )

    # Helper functions
    def calculate_entry_price() -> float:
        threshold = round((data["ST 10 3 UP"] - data["ST 20 5 LOW"]) / 5, 2)
        return threshold + data["ST 20 5 LOW"]

    def create_buy_order(price: float) -> None:
        broker.create_order(
            {
                "id": datetime.now().timestamp(),
                "strategy": "WithDoubleTrend",
                "signal": DoubleTrendSignals.LONG_BUY,
                "order": OrderType.LIMIT_BUY,
                "size": 1,
                "price": price,
            }
        )

    def create_market_sell_order() -> None:
        broker.create_order(
            {
                "id": datetime.now().timestamp(),
                "strategy": "WithDoubleTrend",
                "signal": DoubleTrendSignals.STOP_MARKET,
                "order": OrderType.MARKET_SELL,
                "size": position_size,
            }
        )

    # Case 1: No position - manage entry orders
    if position_size == 0:
        existing_buy_order = next(
            (
                order
                for order in orders
                if order["signal"] == DoubleTrendSignals.LONG_BUY
            ),
            None,
        )

        if existing_buy_order:
            if not condition:
                broker.cancel_order(existing_buy_order["id"])
            else:
                entry_price = calculate_entry_price()
                if existing_buy_order["price"] != entry_price:
                    broker.cancel_order(existing_buy_order["id"])
                    create_buy_order(entry_price)
        elif condition:
            create_buy_order(calculate_entry_price())
        return

    # Case 2: Have position - manage exit conditions
    for order in orders:
        if order["signal"] == DoubleTrendSignals.LONG_BUY:
            broker.cancel_order(order["id"])

    if not condition or is_close_time:
        broker.cancel_all_orders()
        create_market_sell_order()
