from datetime import datetime
import pandas as pd

from myLib.brokers.types import LimitOrderTypedDict, MarketOrderTypedDict, OrderType
from myLib.brokers.demo.positions import Positions


def limit_buy(
    order: LimitOrderTypedDict,
    row: pd.DataFrame,
    index: int,
    position: Positions,
    log: pd.DataFrame,
    orders: list[LimitOrderTypedDict | MarketOrderTypedDict],
):
    """
    Execute a buy limit order based on current market conditions.

    Args:
        order (LimitOrderTypedDict): Details of the limit order to execute
        row (pd.DataFrame): Current market data row
        index (int): Index of the current market data row
        position (Positions): Current trading position object
        log (pd.DataFrame): Logging DataFrame to record trade signals
        orders (list): List of pending orders

    Performs the following actions:
    - Checks if order price is within current market high and low
    - Increases position size if order conditions are met
    - Logs buy signal and price
    - Removes executed order from pending orders
    - Optionally creates a take profit sell order
    """

    if order["price"] <= row["HIGH"] and order["price"] >= row["LOW"]:
        position.increase(order["size"])
        log.loc[index, "SIGNAL"] = order["signal"]
        log.loc[index, "BUY_PRICE"] = order["price"]
        orders[:] = [item for item in orders if item["id"] != order["id"]]

        if "take_profit" in order:
            orders.append(
                {
                    "id": datetime.now().timestamp(),
                    "strategy": order["strategy"],
                    "signal": "TAKE_PROFIT",
                    "order": OrderType.LIMIT_SELL,
                    "price": order["take_profit"],
                    "size": order["size"],
                }
            )
