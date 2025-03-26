"""Main class for Alor broker."""

from .download import AlorDownloader


class Alor:
    """Represents an Alor broker."""

    def __init__(self):
        """Initializes the broker with an AlorDownloader instance."""
        self.downloader = AlorDownloader()
        print("Alor Broker initialized")
