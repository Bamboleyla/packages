from typing import TypedDict
from enum import Enum


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


class DoubleTrendSignals(str, Enum):
    """
    Enumeration of signal types used by the WithDoubleTrend strategy.

    These signals represent different trading actions and conditions:
    - LONG_BUY: Signal to open a long position
    - LONG_CLOSE: Signal to close a long position
    - LONG_TP: Signal when take profit is triggered
    - LONG_SL: Signal when stop loss is triggered
    """

    LONG_BUY = "LONG_BUY"
    LONG_SELL = "LONG_SELL"
    LONG_TP = "LONG_TP"
    LONG_SL = "LONG_SL"
