"""This is init module for demo broker. Demo broker need for testing my strategies"""

from myLib.brokers.types import LimitOrderTypedDict, MarketOrderTypedDict
from myLib.brokers.types import BrokerAbstractClass
from .positions import Positions
from .orders import Orders

__all__ = ["DemoBroker"]


class DemoBroker(BrokerAbstractClass):
    """Class that imitates the work of the broker"""

    def __init__(self) -> None:
        self.__positions = Positions()
        self.__orders = Orders()

    @property
    def name(self) -> str:
        return "DemoBroker"

    def get_positions(self) -> int:
        return self.__positions.get_position()

    def limit_order_buy(self, order: LimitOrderTypedDict) -> None:
        self.__orders.create(order)

    def limit_order_sell(self, order: LimitOrderTypedDict) -> None:
        self.__orders.create(order)

    def marker_order_buy(self, order: MarketOrderTypedDict) -> None:
        self.__orders.create(order)

    def market_order_sell(self, order: MarketOrderTypedDict) -> None:
        self.__orders.create(order)
