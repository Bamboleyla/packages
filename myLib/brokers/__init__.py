"""Main module for all brokers."""

from .alor import Alor
from .demo import DemoBroker
from .types.broker import BrokerAbstractClass
from .types.orders import LimitOrderTypedDict, MarketOrderTypedDict, OrderType

__all__ = [
    "Brokers",
    "BrokerAbstractClass",
    "LimitOrderTypedDict",
    "MarketOrderTypedDict",
    "OrderType",
]


class Brokers:
    """Represents all brokers."""

    def __init__(self):
        """Initializes all brokers."""
        self.alor = Alor()
        self.demo = DemoBroker()
