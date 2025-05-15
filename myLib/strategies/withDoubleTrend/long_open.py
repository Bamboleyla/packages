from datetime import datetime

import pandas as pd
from myLib.brokers import BrokerAbstractClass, OrderType
from ..strategy import StrategyAbstractClass
from .types import SuperTrendParamsTypedDict, DoubleTrendSignals


def long_open_method(
    indicators: dict[str, str],
    broker: BrokerAbstractClass,
    strategy_name: str,
    var_take: float,
    previous: pd.DataFrame,
    current: pd.DataFrame,
) -> None:
    """
    It opens a long position (creates an order for the purchase) when fulfilling conditions
      based on the Supertrend indicators (Fast, Slow).

    Conditions for opening a position:
    1. The closing price of the previous bar (previous["Close"]) should be:
    - below or equal to the value of the fast upper Supertrend (FAST_UP)
    - above the slowly lower Supertrend (Slow_Down)
    2. The opening price of the current bar (Current ["Open"]) should be:
    - above the value of the fast lower Supertrend (FAST_Down)
    - above the slowly lower Supertrend (Slow_Down)

    When fulfilling all conditions:
    - Sent a limit order for the purchase at the price of Fast_up of the previous bar
    - take-profit is installed at the distance self.__var_take from the entrance price
    - stop-loss is not installed

    Args:
        previous (pd.DataFrame): Dataframe with the data of the previous bar (one line)
            Must contain columns:
            - "CLOSE" - Closing price
            - self.__fast_up - Fast upper Supertrend
            - self.__slow_down - Slow lower Supertrend

        current (pd.DataFrame): Dataframe with the data of the current bar (one line)
            Must contain columns:
            - "OPEN" - цена открытия
            - self.__fast_down - Fast lower Supertrend
            - self.__slow_down - Slow lower Supertrend

    Returns:
        None: The method does not return anything, only sends the warrant through the broker
    """

    # We check the conditions at the previous bar (use .iloc [0] since only one line)
    prev_close = previous["CLOSE"]
    prev_fast_up = previous[indicators["fast_up"]]
    prev_slow_down = previous[indicators["slow_down"]]

    # We check the conditions at the current bar
    curr_open = current["OPEN"]
    curr_fast_down = current[indicators["fast_down"]]
    curr_slow_down = current[indicators["slow_down"]]

    # The first condition: checking the position of the closing price relative to indicators
    if (prev_close <= prev_fast_up) and (prev_close > prev_slow_down):

        # Second condition: checking the opening price of the indicators
        if (curr_open > curr_fast_down) and (curr_open > curr_slow_down):

            # The price for the entrance is the FAST_UP value of the previous bar
            entry_price = prev_fast_up

            orders = broker.get_orders()
            # If there are orders, we cancel them
            if len(orders) > 0:
                for order in orders:
                    broker.cancel_order(order["id"])

            # Form and send a order for the purchase
            broker.create_order(
                {
                    "id": datetime.now().timestamp(),  # Unique ID order
                    "strategy": strategy_name,  # The name of the strategy
                    "signal": DoubleTrendSignals.LONG_BUY,  # Signal type
                    "order": OrderType.LIMIT_BUY,  # Type of warrant (limit)
                    "price": entry_price,  # The price of the entrance
                    "size": 1,  # Position size
                    "take_profit": entry_price + var_take,  # TAKE-PROFIT level
                }
            )
