"""
A library for algorithmic trading that provides brokers and strategies.

This module contains:
    - Brokers: Classes for interacting with different trading platforms
    - Strategies: Collection of trading strategy implementations

Example:
    from myLib import Brokers, Strategies
"""

from .brokers import Brokers
from .strategies import Strategies

__all__ = ["Brokers", "Strategies"]
