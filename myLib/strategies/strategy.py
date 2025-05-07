"""
This module defines the base Strategy class and interfaces for implementing trading strategies.

The Strategy class serves as an abstract base class that all concrete trading strategy
implementations must inherit from. It enforces a consistent interface for running
strategy analysis on financial market data.
"""

from abc import ABC, abstractmethod
import pandas as pd

__all__ = ["StrategyAbstractClass"]


class StrategyAbstractClass(ABC):
    """
    Base class for all trading strategies in the library.

    This abstract base class defines the interface for strategy implementations,
    ensuring that all strategies have a consistent method for running analysis
    on financial data.
    """

    @abstractmethod
    def run(self, previous: pd.DataFrame, current: pd.DataFrame) -> None:
        pass
