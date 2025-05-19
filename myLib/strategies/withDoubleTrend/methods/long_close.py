from datetime import datetime

import pandas as pd
from myLib.brokers import OrderType, BrokerAbstractClass
from myLib.strategies.withDoubleTrend.types import DoubleTrendSignals


def long_close_method(
    fast_down_key: str,
    broker: BrokerAbstractClass,
    strategy_name: str,
    row: pd.DataFrame,
) -> None:

    if pd.isna(row[fast_down_key]):

        orders = broker.get_orders()
        # If there are orders, we cancel them
        if len(orders) > 0:
            for order in orders:
                broker.cancel_order(order["id"])

        broker.create_order(
            {
                "id": datetime.now().timestamp(),
                "strategy": strategy_name,
                "signal": DoubleTrendSignals.LONG_TP,
                "order": OrderType.MARKET_SELL,
                "size": 1,
            }
        )
