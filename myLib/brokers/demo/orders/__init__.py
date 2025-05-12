"""
Module for managing trading orders in a demo broker implementation.

This module provides the Orders class for handling various types of trading orders
including limit orders and market orders. It supports operations such as:
- Creating new orders
- Processing limit buy/sell orders
- Executing market buy orders
- Managing market stop orders
- Tracking order history and positions

The module integrates with position management and maintains a log of all order executions.
"""

import pandas as pd
from myLib.brokers.types.orders import LimitOrderTypedDict, MarketOrderTypedDict
from ..positions import Positions
from .order_methods.buy_limit import buy_limit
from .order_methods.sell_limit import sell_limit
from .order_methods.market_buy import market_buy
from .order_methods.market_stop import market_stop

__all__ = ["Orders"]


class Orders:
    """Class for managing orders."""

    def __init__(self):
        self.__orders: list[LimitOrderTypedDict | MarketOrderTypedDict] = []
        self.__log = pd.DataFrame()

    def create(self, order: LimitOrderTypedDict | MarketOrderTypedDict):
        """
        Create a new order by clearing existing orders and adding the specified order.

        Args:
            order (LimitOrderTypedDict | MarketOrderTypedDict): The order to be created and added
              to the orders list.
        """

        self.__orders.clear()
        self.__orders.append(order)

    def run(self, row: pd.DataFrame, index: int, positions: Positions):
        """
        Execute trading orders and manage position closing for a given market data row.

        This method processes pending orders (limit buy, limit sell, market buy)
        and handles end-of-day position closure using market stop orders.

        Args:
            row (pd.DataFrame): Current market data row for order processing.
            index (int): Index of the current market data row.
        """

        # Processing of orders
        if len(self.__orders) > 0:
            for order in self.__orders:
                if order["order"] == "LIMIT_BUY":
                    buy_limit(order, row, index, positions, self.__log, self.__orders)

                elif order["order"] == "LIMIT_SELL":
                    sell_limit(order, row, index, positions, self.__log, self.__orders)

                elif order["order"] == "MARKET_BUY":
                    market_buy(order, row, index, positions, self.__log, self.__orders)
        # Closing positions at the end of the day
        market_stop(row, index, positions, self.__log, self.__orders)

    def get_log(self) -> pd.DataFrame:
        """
        Retrieve the log of orders and their execution details.

        Returns:
            pd.DataFrame: A DataFrame containing the log of order activities.
        """

        return self.__log
