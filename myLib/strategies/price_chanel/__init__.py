from myLib.brokers import BrokerAbstractClass
from .methods.plot_data import plot_data
from .methods.calculate import calculate
from ..strategy import StrategyAbstractClass
import pandas as pd

__all__ = ["PriceChanelGrid"]


class PriceChanelGrid(StrategyAbstractClass):
    def __init__(self, broker: BrokerAbstractClass) -> None:
        super().__init__()
        self.name: str = "PriceChanelGrid"
        self._broker: BrokerAbstractClass = broker
        self._config = {
            "indicators": [
                {"type": "price_chanel", "period": 20},
                {"type": "super_trend", "period": 30, "multiplier": 7},
            ]
        }

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        return calculate(data)

    def get_config(self) -> dict:
        return self._config

    def get_plot_data(self):
        return plot_data()
