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
from myLib.brokers.types.orders import (
    LimitOrderTypedDict,
    MarketOrderTypedDict,
    OrderType,
)
from ..positions import Positions
from .order_methods.limit_buy import limit_buy
from .order_methods.limit_sell import limit_sell
from .order_methods.market_buy import market_buy
from .order_methods.market_sell import market_sell
from .order_methods.market_stop import market_stop

__all__ = ["Orders"]


class Orders:
    """Class for managing orders."""

    def __init__(self):
        self.__orders: list[LimitOrderTypedDict | MarketOrderTypedDict] = []
        self.__log = pd.DataFrame()

    def create(self, order: LimitOrderTypedDict | MarketOrderTypedDict):
        """
        Create a new order and add it to the orders list.

        Args:
            order (LimitOrderTypedDict | MarketOrderTypedDict): The order to be created and added
              to the orders list.
        """

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
                if order["order"] == OrderType.LIMIT_BUY:
                    limit_buy(order, row, index, positions, self.__log, self.__orders)

                elif (
                    order["order"] == OrderType.LIMIT_SELL
                    or order["order"] == OrderType.LONG_TP
                ):
                    limit_sell(order, row, index, positions, self.__log, self.__orders)

                elif order["order"] == OrderType.MARKET_BUY:
                    market_buy(order, row, index, positions, self.__log, self.__orders)

                elif order["order"] == OrderType.MARKET_SELL:
                    market_sell(order, row, index, positions, self.__log, self.__orders)
                else:
                    raise ValueError(
                        f"Unknown order type: {order['order']}. Supported types are: LIMIT_BUY, LIMIT_SELL, MARKET_BUY, MARKET_SELL."
                    )

    def get_log(self) -> pd.DataFrame:
        """
        Retrieve the log of orders and their execution details.

        Returns:
            pd.DataFrame: A DataFrame containing the log of order activities.
        """

        return self.__log

    def get_orders(self) -> list[LimitOrderTypedDict | MarketOrderTypedDict]:
        """
        Retrieve the current list of active orders.

        Returns:
            list[LimitOrderTypedDict | MarketOrderTypedDict]: A list containing the current active orders.
        """

        return self.__orders

    def delete_order(self, order_id: float) -> None:
        """
        Delete an order with the specified order_id from the active orders list.

        Args:
            order_id (float): The ID of the order to be deleted.

        Raises:
            ValueError: If no order with the specified ID is found.
        """
        for order in self.__orders:
            if order["id"] == order_id:
                self.__orders.remove(order)
                return

        # If we get here, no order with the specified ID was found
        raise ValueError(f"Order with ID {order_id} not found")
