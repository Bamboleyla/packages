"""
The module contains the Positions class to manage positions.

Positions class provides methods for obtaining a current position,
And also to increase or decrease it by a given amount.
"""


class Positions:
    """Class for managing and tracking positions"""

    def __init__(self):
        self.__position = 0

    def get_position(self) -> int:
        """Returns the current value of the position.

        Returns:
            int: Current position.
        """
        return self.__position

    def increase(self, quantity: int):
        """Increases the position on a given amount.

        Args:
            quantity (int): the quantity for which the position is increasing.
        """
        self.__position = self.__position + quantity

    def decrease(self, quantity: int):
        """Reduces the position on a given amount.

        Args:
            quantity (int): The quantity for which the position is reduced.
        """
        self.__position = self.__position - quantity
