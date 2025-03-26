"""Main class for all brokers."""

from .alor import Alor


class Brokers:
    """Represents all brokers."""

    def __init__(self):
        """Initializes all brokers."""
        self.alor = Alor()
