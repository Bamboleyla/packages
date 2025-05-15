from datetime import datetime

import pandas as pd
from myLib.brokers import BrokerAbstractClass, OrderType
from ..strategy import StrategyAbstractClass
from .types import SuperTrendParamsTypedDict, DoubleTrendSignals
from .long_close import long_close_method
from .long_open import long_open_method

__all__ = ["WithDoubleTrend"]


class WithDoubleTrend(StrategyAbstractClass):
    def __init__(self, params: SuperTrendParamsTypedDict, broker: BrokerAbstractClass):
        self.name = "WithDoubleTrend"
        self.__var_take = params["var_take"]
        self.__indicators = params["indicators"]
        self.__broker = broker

    def run(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
        positions = self.__broker.get_positions()

        if positions == 0:
            # try to open a long position
            self.__long_open(previous, current)

        elif positions > 0:
            self.__long_close(current)

    def __long_open(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
        long_open_method(
            indicators=self.__indicators,
            broker=self.__broker,
            strategy_name=self.name,
            var_take=self.__var_take,
            previous=previous,
            current=current,
        )

    def __long_close(self, row: pd.DataFrame) -> None:
        long_close_method(self.__indicators["fast_down"], self.__broker, self.name, row)
