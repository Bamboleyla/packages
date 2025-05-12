from datetime import datetime
from typing import TypedDict
import pandas as pd
from myLib.brokers import BrokerAbstractClass
from ..strategy import StrategyAbstractClass

__all__ = ["WithDoubleTrend"]


class SuperTrendParamsTypedDict(TypedDict):
    """
    A TypedDict class which contains the names of the columns with the values of the Supertrend
      indicators.

    The SuperTrend indicator uses two sets of parameters (fast and slow) for trend detection,
    where each set contains upward and downward trend values.

    Attributes:
        fast_up (str): Column name for the fast upward trend calculation.

        fast_down (str): Column name for the fast downward trend calculation.

        slow_up (str): Column name for the slow upward trend calculation.

        slow_down (str): Column name for the slow downward trend calculation.

    Example:
        params = SuperTrendParams(
            fast_up='ST 10 3 UP',
            fast_down='ST 10 3 LOW',
            slow_up='ST 20 5 UP,
            slow_down='ST 20 5 LOW'
        )
    """

    var_take: float
    indicators: dict[str, str]


class WithDoubleTrend(StrategyAbstractClass):
    def __init__(self, params: SuperTrendParamsTypedDict, broker: BrokerAbstractClass):
        self.name = "WithDoubleTrend"
        self.__var_take = params["var_take"]
        self.__fast_up = params["indicators"]["fast_up"]
        self.__fast_down = params["indicators"]["fast_down"]
        self.__slow_up = params["indicators"]["slow_up"]
        self.__slow_down = params["indicators"]["slow_down"]
        self.__broker = broker

    def run(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
        positions = self.__broker.get_positions()

        if positions == 0:
            return self.__long_open(previous, current)

        elif positions > 0:
            return self.__long_close(current)

    def __long_open(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
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
        prev_fast_up = previous[self.__fast_up]
        prev_slow_down = previous[self.__slow_down]

        # We check the conditions at the current bar
        curr_open = current["OPEN"]
        curr_fast_down = current[self.__fast_down]
        curr_slow_down = current[self.__slow_down]

        # The first condition: checking the position of the closing price relative to indicators
        if (prev_close <= prev_fast_up) and (prev_close > prev_slow_down):

            # Second condition: checking the opening price of the indicators
            if (curr_open > curr_fast_down) and (curr_open > curr_slow_down):

                # The price for the entrance is the FAST_UP value of the previous bar
                entry_price = prev_fast_up

                # Form and send a order for the purchase
                self.__broker.limit_order_buy(
                    {
                        "id": datetime.now().timestamp(),  # Unique ID order
                        "strategy": self.name,  # The name of the strategy
                        "message": "LONG_BUY",  # Signal type
                        "order": "LIMIT_BUY",  # Type of warrant (limit)
                        "price": entry_price,  # The price of the entrance
                        "size": 1,  # Position size
                        "take_profit": entry_price
                        + self.__var_take,  # TAKE-PROFIT level
                    }
                )

    def __long_close(self, row: pd.DataFrame) -> None:
        if pd.isna(row[self.__fast_down]):
            self.__broker.market_order_sell(
                {
                    "id": datetime.now().timestamp(),
                    "strategy": self.name,
                    "message": "LONG_CLOSE",
                    "order": "MARKET_SELL",
                    "size": 1,
                }
            )
