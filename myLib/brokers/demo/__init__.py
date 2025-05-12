"""This is init module for demo broker. Demo broker need for testing my strategies"""

import pandas as pd
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

    def run(self, row: pd.DataFrame, index: int) -> None:
        self.__orders.run(row=row, index=index, positions=self.__positions)

    def get_positions(self) -> int:
        return self.__positions.get_position()

    def get_orders_log(self) -> pd.DataFrame:
        return self.__orders.get_log()

    def limit_order_buy(self, order: LimitOrderTypedDict) -> None:
        self.__orders.create(order)

    def limit_order_sell(self, order: LimitOrderTypedDict) -> None:
        self.__orders.create(order)

    def marker_order_buy(self, order: MarketOrderTypedDict) -> None:
        self.__orders.create(order)

    def market_order_sell(self, order: MarketOrderTypedDict) -> None:
        self.__orders.create(order)
