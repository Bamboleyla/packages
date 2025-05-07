"""This file stores typified dictionaries for class Broker"""

from typing import NotRequired, TypedDict, Literal


class LimitOrderTypedDict(TypedDict):
    """Dictionary describing the limit order in the trading system.

    Attributes:
        id (datetime): Identifier in the form of a temporary mark.
        strategy (str): The name of the strategy by which the order was created.
        message (str): The signal that initiated the order.
        order (Literal["LIMIT_BUY", "LIMIT_SELL"]): Type of order.
            Order description:
                - "LIMIT_BUY" - Limitable order for buy
                - "LIMIT_SELL" - Limitable order for sale
        price (float): The price of which the order is located.
        size (int): Order size (number of asset units).
        take_profit (None | float): Price for making profit (take-profit).
            None, If not installed.
        stop_loss (None | float): Price to restrict losses (stop-loss).
            None, If not installed.
    """

    id: float
    strategy: str
    message: str
    order: Literal["LIMIT_BUY", "LIMIT_SELL"]
    price: float
    size: int
    take_profit: NotRequired[float]
    stop_loss: NotRequired[float]


class MarketOrderTypedDict(TypedDict):
    """Dictionary describing the market order in the trading system.

    Attributes:
        id (float): Identifier in the form of a temporary mark.
        strategy (str): The name of the strategy by which the order was created.
        message (str): The signal that initiated the order.
        order (Literal["MARKET_BUY", "MARKET_SELL"]): Type of order.
            Order description:
                - "MARKET_BUY" - Market order for buy
                - "MARKET_SELL" - Market order for sale
        size (int): Order size (number of asset units).
    """

    id: float
    strategy: str
    message: str
    order: Literal["MARKET_BUY", "MARKET_SELL"]
    size: int
