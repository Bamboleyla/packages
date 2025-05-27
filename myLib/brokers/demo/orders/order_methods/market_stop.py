"""
Market Stop Order Module

This module provides functionality for executing market stop orders at the end of the trading day.
It contains a market_stop function that automatically closes all open long positions
at a specified time (23:45:00) by executing market orders.

The module is part of the demo broker implementation and works with position management,
logging, and order handling systems.

Functions:
    market_stop: Executes market stop orders to close positions at day end.
"""

import pandas as pd

from myLib.brokers.types import LimitOrderTypedDict, MarketOrderTypedDict
from myLib.brokers.demo.positions import Positions


def market_stop(
    row: pd.DataFrame,
    index: int,
    position: Positions,
    log: pd.DataFrame,
    orders: list[LimitOrderTypedDict | MarketOrderTypedDict],
):
    """
    Execute a market stop order at the end of the trading day.

    Closes all open long positions at 23:45:00 by decreasing the position to zero,
    logging the market stop signal, and recording the sell price from the open price.

    Args:
        row (pd.DataFrame): Current row of trading data.
        index (int): Current index in the log DataFrame.
        position (Positions): Position management object.
        log (pd.DataFrame): Logging DataFrame to record trade signals.
        orders (list[LimitOrderTypedDict | MarketOrderTypedDict]): List of active orders.
    """

    positions = position.get_position()["size"]
    if (
        positions > 0
        and pd.to_datetime(row["DATE"]).time() == pd.Timestamp("23:45:00").time()
    ):
        position.decrease(quantity=positions, price=row["OPEN"])
        log.loc[index, "SIGNAL"] = "MARKET_STOP"
        log.loc[index, "SELL_PRICE"] = row["OPEN"]
        orders.clear()
