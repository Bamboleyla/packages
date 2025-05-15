import pandas as pd
from myLib.brokers.types import LimitOrderTypedDict, MarketOrderTypedDict
from myLib.brokers.demo.positions import Positions


def market_sell(
    order: LimitOrderTypedDict,
    row: pd.DataFrame,
    index: int,
    position: Positions,
    log: pd.DataFrame,
    orders: MarketOrderTypedDict,
):
    position.decrease(order["size"])
    log.loc[index, "SIGNAL"] = order["signal"]
    log.loc[index, "SELL_PRICE"] = row["CLOSE"]
    orders[:] = [item for item in orders if item["id"] != order["id"]]
