from enum import Enum


class PriceChanelGridSignals(str, Enum):
    """
    Enumeration of signal types used by the PriceChanelGrid strategy.

    These signals represent different trading actions and conditions:
    - LONG_BUY: Signal to open a long position
    - LONG_CLOSE: Signal to close a long position
    - LONG_TP: Signal when take profit is triggered
    - LONG_SL: Signal when stop loss is triggered
    - STOP_MARKET: Signal to close a position, because trading time ends
    """

    LONG_BUY = "LONG_BUY"
    LONG_SELL = "LONG_SELL"
    LONG_TP = "LONG_TP"
    LONG_SL = "LONG_SL"
    STOP_MARKET = "STOP_MARKET"
