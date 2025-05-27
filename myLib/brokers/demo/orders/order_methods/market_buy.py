"""
This module contains the market_buy function for executing market buy orders
in a demo trading environment.

The module provides functionality to:
- Execute market buy orders at current market prices
- Update position sizes
- Log trade signals and execution prices
- Manage active order lists

The market_buy function is used as part of the demo broker implementation to simulate
real market order execution for buy-side trades.
"""

import pandas as pd
from myLib.brokers.types.orders import LimitOrderTypedDict, MarketOrderTypedDict
from myLib.brokers.demo.positions import Positions


def market_buy(
    order: MarketOrderTypedDict,
    row: pd.DataFrame,
    index: int,
    position: Positions,
    log: pd.DataFrame,
    orders: list[LimitOrderTypedDict | MarketOrderTypedDict],
):
    """
    Execute a market buy order for a given position.

    Args:
        order (MarketOrderTypedDict): The market order details to be executed.
        row (pd.DataFrame): The current market data row.
        index (int): The current index in the dataset.
        position (Positions): The current trading position object.
        log (pd.DataFrame): The trading log to record order details.
        orders (list[LimitOrderTypedDict | MarketOrderTypedDict]): List of active orders.

    Performs the following actions:
    - Increases the trading position by the order size
    - Logs the buy signal and buy price
    - Removes the executed order from the active orders list
    """
    position.increase(order["size"])
    log.loc[index, "SIGNAL"] = order["message"]
    log.loc[index, "BUY_PRICE"] = row["OPEN"].iloc[0]
    orders[:] = [item for item in orders if item["id"] != order["id"]]
