"""
Sell limit order execution module for demo broker.

This module provides functionality to execute sell limit orders in a simulated trading environment.
It contains methods to process sell limit orders based on price conditions and update positions
and trading logs accordingly.

The main function:
- sell_limit: Executes a sell limit order when price conditions are met

The module works with the following data structures:
- LimitOrderTypedDict: Dictionary containing limit order details
- MarketOrderTypedDict: Dictionary containing market order details
- Positions: Class managing trading positions
- DataFrame: Pandas DataFrame for price data and logging
"""

import pandas as pd
from myLib.brokers.types import LimitOrderTypedDict, MarketOrderTypedDict
from myLib.brokers.demo.positions import Positions


def limit_sell(
    order: LimitOrderTypedDict,
    row: pd.DataFrame,
    index: int,
    position: Positions,
    log: pd.DataFrame,
    orders: list[LimitOrderTypedDict | MarketOrderTypedDict],
):
    """
    Execute a sell limit order when the current price is within the specified price range.

    Args:
        order (LimitOrderTypedDict): The limit sell order details.
        row (pd.DataFrame): The current price data row.
        index (int): The current index in the data.
        position (Positions): The current trading positions.
        log (pd.DataFrame): The trading log to record signals and prices.
        orders (list[LimitOrderTypedDict | MarketOrderTypedDict]): The list of active orders.

    Performs the following actions:
    - Checks if the order price is within the current price range (HIGH and LOW)
    - Decreases the position size if the order conditions are met
    - Logs the sell signal and sell price
    - Removes the executed order from the active orders list
    """

    if order["price"] <= row["HIGH"] and order["price"] >= row["LOW"]:
        position.decrease(quantity=order["size"], price=order["price"])
        log.loc[index, "SIGNAL"] = order["signal"]
        log.loc[index, "SELL_PRICE"] = order["price"]
        orders[:] = [item for item in orders if item["id"] != order["id"]]
