import pandas as pd
import os

from .methods.get_history import get_history
from .methods.get_candles import get_candles
from .methods.get_positions import get_positions
from .methods.get_orders import get_orders
from .methods.post_order import post_order
from .methods.replace_order import replace_order
from .methods.cancel_order import cancel_order
from .methods.post_stop_order import post_stop_order
from .methods.get_portfolio import get_portfolio
from .methods.get_operations import get_operations

__all__ = ["Tinkoff"]


class Tinkoff:
    """Represents a Tinkoff broker."""

    def __init__(self):
        self.name = "Tinkoff"
        self.token = os.getenv("TINKOFF_TOKEN")
        self.account_id = os.getenv("TINKOFF_ACCOUNT_ID")
        self.request_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_candles(
        self,
        instrument_id: str,
        start_date: str,
        end_date: str,
        interval: str = "CANDLE_INTERVAL_5_MIN",
        is_complete: bool = True,
    ) -> pd.DataFrame:
        return get_candles(
            self, instrument_id, start_date, end_date, interval, is_complete
        )

    def get_positions(self):
        return get_positions(self)

    def get_orders(self, figi: str):
        return get_orders(self, figi)

    def create_limit_buy_order(self, price: float, instrument_id: str, quantity: int):
        return post_order(
            self=self,
            order_type="ORDER_TYPE_LIMIT",
            instrument_id=instrument_id,
            quantity=quantity,
            price=price,
            direction="ORDER_DIRECTION_BUY",
        )

    def create_limit_sell_order(self, price: float, instrument_id: str, quantity: int):
        return post_order(
            self=self,
            order_type="ORDER_TYPE_LIMIT",
            instrument_id=instrument_id,
            quantity=quantity,
            price=price,
            direction="ORDER_DIRECTION_SELL",
        )

    def create_market_buy_order(self, instrument_id: str, quantity: int):
        return post_order(
            self=self,
            order_type="ORDER_TYPE_MARKET",
            instrument_id=instrument_id,
            quantity=quantity,
            direction="ORDER_DIRECTION_BUY",
            price=None,
        )

    def create_market_sell_order(self, instrument_id: str, quantity: int):
        return post_order(
            self=self,
            order_type="ORDER_TYPE_MARKET",
            instrument_id=instrument_id,
            quantity=quantity,
            direction="ORDER_DIRECTION_SELL",
            price=None,
        )

    def replace_order(
        self, order_id: str, price: float, instrument_id: str, quantity: int
    ):
        return replace_order(
            self,
            order_id=order_id,
            instrument_id=instrument_id,
            quantity=quantity,
            price=price,
        )

    def cancel_order(self, order_id: str):
        return cancel_order(
            self,
            order_id=order_id,
        )

    def create_long_stop_loss_order(
        self, price: float, instrument_id: str, quantity: int
    ):
        return post_stop_order(
            self=self,
            stop_order_type="STOP_ORDER_TYPE_STOP_LOSS",
            instrument_id=instrument_id,
            quantity=quantity,
            price=price,
            direction="STOP_ORDER_DIRECTION_SELL",
        )

    def create_long_take_profit_order(
        self, price: float, instrument_id: str, quantity: int
    ):
        return post_stop_order(
            self=self,
            stop_order_type="STOP_ORDER_TYPE_TAKE_PROFIT",
            instrument_id=instrument_id,
            quantity=quantity,
            price=price,
            direction="STOP_ORDER_DIRECTION_SELL",
        )

    def get_portfolio(self):
        return get_portfolio(self)

    def get_operations(self, figi, from_date):
        return get_operations(self, figi, from_date)
