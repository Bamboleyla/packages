from datetime import datetime
import pandas as pd
from myLib.brokers import OrderType, BrokerAbstractClass
from ..strategy import StrategyAbstractClass
from .types import SuperTrendParamsTypedDict, DoubleTrendSignals
from ..types.plot_data import PlotDataTypedDict
from .methods.long_close import long_close_method
from .methods.long_open import long_open_method
from .methods.plot_data import plot_data


__all__ = ["WithDoubleTrend", "PlotDataTypedDict"]


class WithDoubleTrend(StrategyAbstractClass):
    def __init__(self, params: SuperTrendParamsTypedDict, broker: BrokerAbstractClass):
        self.name = "WithDoubleTrend"
        self.__var_take = params["var_take"]
        self.__indicators = params["indicators"]
        self.__broker = broker

    def run(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
        positions = self.__broker.get_positions()
        orders = self.__broker.get_orders()

        if positions["size"] == 0:
            # If there are orders (Take-Profit or Stop-Loss), we cancel them
            if len(orders) > 0:
                for order in orders:
                    if (
                        order["signal"] == DoubleTrendSignals.LONG_TP
                        or order["signal"] == DoubleTrendSignals.LONG_SL
                    ):
                        self.__broker.cancel_order(order["id"])
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
            # check work time, if it is 23:45:00, then close the position
            if (
                pd.to_datetime(current["DATE"]).time()
                == pd.Timestamp("23:45:00").time()
            ):
                self.__broker.create_order(
                    {
                        "id": datetime.now().timestamp(),
                        "strategy": self.name,
                        "signal": DoubleTrendSignals.STOP_MARKET,
                        "order": OrderType.MARKET_SELL,
                        "size": positions["size"],
                    }
                )
            # check if the position has a take profit order, if not, create it
            else:
                if not any(
                    order.get("signal") == DoubleTrendSignals.LONG_TP
                    for order in orders
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
        else:
            raise ValueError("Position size is not correct.")

    def get_plot_data(self) -> PlotDataTypedDict:
        return plot_data()
