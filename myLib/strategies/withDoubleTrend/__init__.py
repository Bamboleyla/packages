from datetime import datetime
import pandas as pd
from myLib.brokers import OrderType, BrokerAbstractClass
from ..strategy import StrategyAbstractClass
from .types import SuperTrendParamsTypedDict, DoubleTrendSignals
from .methods.long_close import long_close_method
from .methods.long_open import long_open_method

__all__ = ["WithDoubleTrend"]


class WithDoubleTrend(StrategyAbstractClass):
    def __init__(self, params: SuperTrendParamsTypedDict, broker: BrokerAbstractClass):
        self.name = "WithDoubleTrend"
        self.__var_take = params["var_take"]
        self.__indicators = params["indicators"]
        self.__broker = broker

    def run(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
        positions = self.__broker.get_positions()

        if positions["size"] == 0:
            # try to open a long position
            long_open_method(
                indicators=self.__indicators,
                broker=self.__broker,
                strategy_name=self.name,
                var_take=self.__var_take,
                previous=previous,
                current=current,
            )

        elif positions["size"] > 0:
            orders = self.__broker.get_orders()
            if not any(
                order.get("signal") == DoubleTrendSignals.LONG_TP for order in orders
            ):
                self.__broker.create_order(
                    {
                        "id": datetime.now().timestamp(),
                        "strategy": self.name,
                        "signal": DoubleTrendSignals.LONG_TP,
                        "order": OrderType.LONG_TP,
                        "size": positions["size"],
                        "price": positions["average_price"] + self.__var_take,
                    }
                )
            # try to close a long position
            long_close_method(
                self.__indicators["fast_down"], self.__broker, self.name, current
            )
