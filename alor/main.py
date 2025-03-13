"""Main class for Alor broker."""

from .download import AlorDownloader


class Alor:
    """This class represents an Alor broker."""

    def __init__(self):
        downloader = AlorDownloader()

        self.downloader = downloader
        print("Alor Broker initialized")
