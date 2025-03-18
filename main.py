"""Main module for the package."""

from alor import Broker


class Packages:
    """This class manages packages."""

    def __init__(self):
        broker = Broker()

        self.alor = broker
        print("Packages class initialized")


if __name__ == "__main__":
    print(__name__)
    packages = Packages()
