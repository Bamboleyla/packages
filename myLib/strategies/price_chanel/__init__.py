from myLib.brokers import BrokerAbstractClass
from .methods.plot_data import plot_data
from .methods.calculate import calculate
from .methods.run import run
from ..strategy import StrategyAbstractClass
import pandas as pd

__all__ = ["PriceChanelGrid"]


class PriceChanelGrid(StrategyAbstractClass):
    def __init__(self, broker: BrokerAbstractClass, config: dict) -> None:
        super().__init__()
        self.name: str = "PriceChanelGrid"
        self._broker: BrokerAbstractClass = broker
        self._config = config
        self._order = None
        self._take_profit = None
        self._stop_loss = None
        self._last_buy_price = None
        self._from_date = (
            pd.Timestamp.now().normalize().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        )
        self._figi = config["share"]["figi"]

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        return run(self, df)

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        return calculate(data, self._config["indicators"])

    def get_config(self) -> dict:
        return self._config

    def get_indicators_params(self) -> dict:
        indicators = self._config["indicators"]
        pc_period = indicators[0]["period"]
        st_period = indicators[1]["period"]
        st_multiplier = indicators[1]["multiplier"]
        return pc_period, st_period, st_multiplier

    def get_plot_data(self):
        return plot_data(self)
