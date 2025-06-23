from myLib.brokers import BrokerAbstractClass
from .methods.plot_data import plot_data
from ..strategy import StrategyAbstractClass
import pandas as pd


__all__ = ["PriceChanelGrid"]


class PriceChanelGrid(StrategyAbstractClass):
    def __init__(self, broker: BrokerAbstractClass) -> None:
        super().__init__()
        self.name: str = "PriceChanelGrid"
        self._broker: BrokerAbstractClass = broker
        self._config = {"indicators": [{"type": "price_chanel", "period": 20}]}

    def run(self, current: pd.DataFrame, previous: pd.DataFrame) -> None:
        """Combines position management (TP, SL and basic logic)"""
        positions = self._broker.get_positions()
        orders = self._broker.get_orders()

    def get_config(self) -> dict:
        """Returns strategy config"""
        return self._config

    def get_plot_data(self):
        return plot_data()
