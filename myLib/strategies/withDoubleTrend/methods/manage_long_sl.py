from datetime import datetime
import pandas as pd
from myLib.brokers import BrokerAbstractClass, LimitOrderTypedDict, OrderType
from ..types import DoubleTrendSignals


def manage_long_sl(
    positions: dict[str, int],
    broker: BrokerAbstractClass,
    data: pd.DataFrame,
    orders: LimitOrderTypedDict,
) -> None:
    """Manage stop-loss orders for long positions.

    Args:
        positions: Dictionary containing position size ('size' key)
        broker: Broker instance for order management
        data: Market data containing stop-loss level ('ST 20 5 LOW' column)
        orders: List of current pending orders
    """
    position_size = positions.get("size", 0)

    # Helper function to create a new stop-loss order
    def create_new_sl_order(stop_loss_price: float) -> None:
        broker.create_order(
            {
                "id": datetime.now().timestamp(),
                "strategy": "WithDoubleTrend",
                "signal": DoubleTrendSignals.LONG_SL,
                "order": OrderType.LONG_SL,
                "size": position_size,
                "price": stop_loss_price,
            }
        )

    # Case 1: No position - cancel all SL orders
    if position_size == 0:
        for order in orders:
            if order["signal"] == DoubleTrendSignals.LONG_SL:
                broker.cancel_order(order["id"])
        return

    # Case 2: Have position - manage SL orders
    stop_loss_price = data.get("ST 20 5 LOW")

    # Find existing SL order if any
    existing_sl_order = next(
        (order for order in orders if order["signal"] == DoubleTrendSignals.LONG_SL),
        None,
    )

    # If no stop loss price available, cancel existing order if any
    if pd.isna(stop_loss_price):
        if existing_sl_order:
            broker.cancel_order(existing_sl_order["id"])
        return

    # If we have position and valid stop loss price
    if existing_sl_order:
        # Update order if price has changed
        if existing_sl_order["price"] != stop_loss_price:
            broker.cancel_order(existing_sl_order["id"])
            create_new_sl_order(stop_loss_price)
    else:
        # Create new SL order if none exists
        create_new_sl_order(stop_loss_price)
