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
from .price_chanel import PriceChanelGrid
from .strategy import StrategyAbstractClass
from .types.plot_data import PlotDataTypedDict

__all__ = [
    "StrategyAbstractClass",
    "PlotDataTypedDict",
    "WithDoubleTrend",
    "PriceChanelGrid",
]
