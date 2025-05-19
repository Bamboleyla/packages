"""This module defines typed dictionaries for trading orders used by the Broker class.

The module provides strongly-typed dictionaries for limit and market orders using Python's TypedDict,
along with an Enum for order type constants. This ensures type safety and clear documentation
of order structures throughout the trading system.
"""

from typing import TypedDict, Literal
from enum import Enum


class OrderType(str, Enum):
    """Enumeration of all possible order types in the trading system.

    Values:
        LIMIT_BUY: Limit buy order
        LIMIT_SELL: Limit sell order
        MARKET_BUY: Market buy order
        MARKET_SELL: Market sell order
        LONG_TP: Long take-profit order
        LONG_SL: Long stop-loss order
    """

    LIMIT_BUY = "LIMIT_BUY"
    LIMIT_SELL = "LIMIT_SELL"
    MARKET_BUY = "MARKET_BUY"
    MARKET_SELL = "MARKET_SELL"
    LONG_TP = "LONG_TP"
    LONG_SL = "LONG_SL"


class BaseOrderTypedDict(TypedDict):
    """Base typed dictionary with common fields for all order types.

    Attributes:
        id: Unique identifier for the order (timestamp in float format)
        strategy: Name of the strategy that generated this order
        signal: Trading signal that triggered this order
        size: Number of asset units to buy/sell
    """

    id: float
    strategy: str
    signal: str
    size: int


class LimitOrderTypedDict(BaseOrderTypedDict):
    """Typed dictionary representing a limit order in the trading system.

    A limit order is an order to buy or sell an asset at a specified price or better.

    Attributes:
        order: Type of limit order (LIMIT_BUY or LIMIT_SELL)
        price: Limit price at which the order should be executed
    """

    order: Literal[OrderType.LIMIT_BUY, OrderType.LIMIT_SELL]
    price: float


class MarketOrderTypedDict(BaseOrderTypedDict):
    """Typed dictionary representing a market order in the trading system.

    A market order is an order to buy or sell an asset immediately at the best available current price.

    Attributes:
        order: Type of market order (MARKET_BUY or MARKET_SELL)
    """

    order: Literal[OrderType.MARKET_BUY, OrderType.MARKET_SELL]
