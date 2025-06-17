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
    curr: pd.DataFrame,
    prev: pd.DataFrame,
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
    condition_1 = (
        pd.notna(curr.get("ST 10 3 LOW"))
        and pd.notna(curr.get("ST 20 5 LOW"))
        and pd.notna(prev.get("ST 20 5 UP"))
    )
    condition_2 = (
        pd.notna(curr.get("ST 10 3 LOW"))
        and pd.notna(curr.get("ST 20 5 LOW"))
        and pd.notna(prev.get("ST 10 3 UP"))
    )

    is_close_time = (
        pd.to_datetime(curr.get("DATE")).time() == pd.Timestamp("23:40:00").time()
    )
    is_open_time = (
        pd.to_datetime(curr.get("DATE")).time() == pd.Timestamp("09:30:00").time()
    )

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
            if pd.isna(curr.get("ST 10 3 LOW")):
                broker.cancel_order(existing_buy_order["id"])
        elif condition_1:
            create_buy_order(prev.get("ST 20 5 UP"))
        elif condition_2:
            create_buy_order(prev.get("ST 10 3 UP"))
        return

    # Case 2: Have position - manage exit conditions
    for order in orders:
        if order["signal"] == DoubleTrendSignals.LONG_BUY:
            broker.cancel_order(order["id"])

    if (
        pd.isna(curr.get("ST 10 3 LOW"))
        and pd.isna(curr.get("ST 20 5 LOW"))
        or is_close_time
    ):
        broker.cancel_all_orders()
        create_market_sell_order()
