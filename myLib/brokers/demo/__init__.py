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

    def create_order(self, order: LimitOrderTypedDict | MarketOrderTypedDict) -> None:
        self.__orders.create(order)

    def get_orders(self) -> list[LimitOrderTypedDict | MarketOrderTypedDict]:
        return self.__orders.get_orders()

    def cancel_order(self, order_id: float) -> None:
        self.__orders.delete_order(order_id)
