"""
This module provides access to various trading strategies.

The strategies module contains different trading strategy implementations that can be used
for analyzing and executing trades based on technical indicators and market conditions.

Available Strategies:
    - WithDoubleTrend: A strategy that utilizes two supertrend indicators for trend analysis

Usage:
    from myLib.strategies import Strategies
    strategies = Strategies()
    double_trend = strategies.double_super_trend
"""

from .withDoubleTrend import WithDoubleTrend
from .strategy import StrategyAbstractClass
from .types.plot_data import PlotDataTypedDict

__all__ = ["Strategies", "StrategyAbstractClass", "PlotDataTypedDict"]


class Strategies:
    """
    A collection of trading strategies for market analysis and trade execution.

    This class provides access to various trading strategies implemented in the library.
    Strategies can be instantiated and used for different trading approaches.

    Attributes:
        double_super_trend (WithDoubleTrend): A strategy utilizing two supertrend indicators
        for comprehensive trend analysis.
    """

    def __init__(self):
        self.double_super_trend = WithDoubleTrend
