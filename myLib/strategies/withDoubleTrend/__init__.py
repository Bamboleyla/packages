import pandas as pd
from myLib.brokers import BrokerAbstractClass
from ..strategy import StrategyAbstractClass
from ..types.plot_data import PlotDataTypedDict
from .methods.manage_long import manage_long
from .methods.plot_data import plot_data
from .methods.manage_long_sl import manage_long_sl
from .methods.manage_long_tp import manage_long_tp


__all__ = ["WithDoubleTrend", "PlotDataTypedDict"]


class WithDoubleTrend(StrategyAbstractClass):
    def __init__(self, broker: BrokerAbstractClass) -> None:
        super().__init__()
        self.name: str = "WithDoubleTrend"
        self._broker: BrokerAbstractClass = broker

    def _manage_positions(self, current: pd.DataFrame) -> None:
        """Combines position management (TP, SL and basic logic)"""
        positions = self._broker.get_positions()
        orders = self._broker.get_orders()

        # The call procedure is important: first tp, then SL, then the main logic
        manage_long_tp(
            positions=positions,
            broker=self._broker,
            data=current,
            orders=orders,
        )
        manage_long_sl(
            positions=positions,
            broker=self._broker,
            data=current,
            orders=orders,
        )
        manage_long(
            positions=positions,
            broker=self._broker,
            data=current,
            orders=orders,
        )

    def run(self, current: pd.DataFrame) -> None:
        """The main method of strategy for processing new data"""
        self._manage_positions(current)

    def get_plot_data(self) -> PlotDataTypedDict:
        """Returns data for visualization"""
        return plot_data()
