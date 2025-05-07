"""Main class for all brokers.

This file provides the abstract base class for broker implementations and
exports the main Brokers class. It defines the fundamental interface that all
concrete broker implementations must follow.
"""

from abc import ABC, abstractmethod

from .orders import LimitOrderTypedDict, MarketOrderTypedDict


class BrokerAbstractClass(ABC):
    """Abstract base class defining the interface for all broker implementations.

    This class specifies the mandatory methods that concrete broker classes must implement
    to support basic trading operations including opening/closing long and short positions.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_positions(self) -> int:
        """Retrieve all currently open positions.

        Returns:
            Information about all open positions. The exact return type depends on
            the concrete implementation.
        """

    @abstractmethod
    def limit_order_buy(self, order: LimitOrderTypedDict) -> None:
        pass

    @abstractmethod
    def limit_order_sell(self, order: LimitOrderTypedDict) -> None:
        pass

    @abstractmethod
    def marker_order_buy(self, order: MarketOrderTypedDict) -> None:
        pass

    @abstractmethod
    def market_order_sell(self, order: MarketOrderTypedDict) -> None:
        pass
