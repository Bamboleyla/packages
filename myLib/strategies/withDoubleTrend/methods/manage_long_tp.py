from datetime import datetime
import pandas as pd
from myLib.brokers import BrokerAbstractClass, LimitOrderTypedDict, OrderType
from ..types import DoubleTrendSignals


def manage_long_tp(
    positions: dict[str, int],
    broker: BrokerAbstractClass,
    data: pd.DataFrame,
    orders: LimitOrderTypedDict,
) -> None:
    """Manage take-profit orders for long positions.

    Args:
        positions: Dictionary containing position size ('size' key)
        broker: Broker instance for order management
        data: Market data containing take-profit level ('ST 10 3 UP' column)
        orders: List of current pending orders
    """
    position_size = positions.get("size", 0)

    # Helper function to create a new take-profit order
    def create_new_tp_order(take_profit_price: float) -> None:
        broker.create_order(
            {
                "id": datetime.now().timestamp(),
                "strategy": "WithDoubleTrend",
                "signal": DoubleTrendSignals.LONG_TP,
                "order": OrderType.LONG_TP,
                "size": position_size,
                "price": take_profit_price,
            }
        )

    # Case 1: No position - cancel all TP orders
    if position_size == 0:
        for order in orders:
            if order["signal"] == DoubleTrendSignals.LONG_TP:
                broker.cancel_order(order["id"])
        return

    # Case 2: Have position - manage TP orders
    take_profit_price = data.get("ST 10 3 UP")

    # Find existing TP order if any
    existing_tp_order = next(
        (order for order in orders if order["signal"] == DoubleTrendSignals.LONG_TP),
        None,
    )

    # If no take profit price available, cancel existing order if any
    if pd.isna(take_profit_price):
        if existing_tp_order:
            broker.cancel_order(existing_tp_order["id"])
        return

    # If we have position and valid take profit price
    if existing_tp_order:
        # Update order if price has changed
        if existing_tp_order["price"] != take_profit_price:
            broker.cancel_order(existing_tp_order["id"])
            create_new_tp_order(take_profit_price)
    else:
        # Create new TP order if none exists
        create_new_tp_order(take_profit_price)
