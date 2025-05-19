"""
The module contains the Positions class to manage positions.

Positions class provides methods for obtaining a current position,
And also to increase or decrease it by a given amount.
"""


class Positions:
    """Class for managing and tracking positions"""

    def __init__(self):
        self.__position = {"size": 0, "average_price": 0}

    def get_position(self) -> dict:
        """Returns the current value of the position.

        Returns:
            dict: Current position with size and average_price.
        """
        return self.__position

    def increase(self, quantity: int, price: float):
        """Increases the position on a given amount.

        Args:
            quantity (int): the quantity for which the position is increasing.
            price (float): the price at which the position is increasing.
        """
        if self.__position["size"] == 0:
            self.__position["size"] += quantity
            self.__position["average_price"] = price
        elif self.__position["size"] + quantity == 0:
            self.__position["size"] = 0
            self.__position["average_price"] = 0
        elif self.__position["size"] > 0:
            total_value = self.__position["size"] * self.__position["average_price"]
            total_value += quantity * price
            new_size = self.__position["size"] + quantity
            self.__position["average_price"] = total_value / new_size
            self.__position["size"] = new_size
        else:
            self.__position["size"] += quantity

    def decrease(self, quantity: int, price: float):
        """Reduces the position on a given amount.

        Args:
            quantity (int): The quantity for which the position is reduced.
        """
        if self.__position["size"] == 0:
            self.__position["size"] -= quantity
            self.__position["average_price"] = price
        elif self.__position["size"] - quantity == 0:
            self.__position["size"] = 0
            self.__position["average_price"] = 0
        elif self.__position["size"] < 0:
            total_value = self.__position["size"] * self.__position["average_price"]
            total_value -= quantity * price
            new_size = self.__position["size"] - quantity
            self.__position["average_price"] = total_value / new_size
            self.__position["size"] = new_size
        else:
            self.__position["size"] -= quantity
