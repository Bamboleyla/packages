"""Main module for all brokers."""

from .alor import Alor
from .demo import DemoBroker
from .types.broker import BrokerAbstractClass
from .types.orders import LimitOrderTypedDict, MarketOrderTypedDict

__all__ = [
    "Brokers",
    "BrokerAbstractClass",
    "LimitOrderTypedDict",
    "MarketOrderTypedDict",
]

demo_broker = DemoBroker()


class Brokers:
    """Represents all brokers."""

    def __init__(self):
        """Initializes all brokers."""
        self.alor = Alor()
        self.demo = demo_broker
